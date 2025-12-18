import boto3 # type: ignore
from urllib.parse import unquote_plus
import json
from datetime import datetime as dt
import os
import uuid
import re

# Get current date for S3 folder name:
today = dt.now().strftime("%Y%m%d")

# S3 client to read/write files
s3 = boto3.client('s3')

# Transcribe client to read job results
ts_client = boto3.client('transcribe')

def lambda_handler(event, context):
    """
    Entrypoint for the transcribe Lambda function. Pulls batch of messages from SQS standard queue.
    """
    print("audio_to_transcribe.lambda_handler started")

    s3bucketOutput = os.environ["BUCKET"]
    batch_failures = []
    for record in event["Records"]:
        event_message = json.loads(record["body"])
        print(f"Event message: {event_message}")

        recordZero = event_message['Records'][0]
        # unquote_plus to handle spaces
        s3object = unquote_plus(recordZero['s3']['object']['key'])
        s3bucketInput = recordZero['s3']['bucket']['name']

        s3Path = "s3://" + s3bucketInput + "/" + s3object
        prefix = os.environ.get('PREFIX', 'ats')
        clean_object = re.sub('[^a-zA-Z0-9_\-.]+','_', s3object)
        jobName = f"{prefix}-{clean_object}-{str(uuid.uuid4())}"
        pii_redaction = os.environ.get('PII_REDACTION', 'false').lower() == 'true'

        try:
            job_params = {
                'TranscriptionJobName': jobName,
                'Settings': {
                    'ShowSpeakerLabels': True,
                    'MaxSpeakerLabels': 10,
                },
                'Media': {
                    'MediaFileUri': s3Path
                },
                'OutputBucketName': s3bucketOutput,
                'OutputKey': today + "/"
            }
            
            if pii_redaction:
                job_params['IdentifyMultipleLanguages'] = False
                job_params['IdentifyLanguage'] = True
                job_params['ContentRedaction'] = {
                    'RedactionType': 'PII',
                    'RedactionOutput': 'redacted_and_unredacted',
                    'PiiEntityTypes': ['ALL']
                }
            else:
                job_params['IdentifyMultipleLanguages'] = True
            
            response = ts_client.start_transcription_job(**job_params)
            print(response)
        except Exception as e:
            print(e)
            batch_failures.append({"itemIdentifier": record["messageId"]})
            continue

    # Send failed messages back to queue for retry
    sqs_response = {}
    if len(batch_failures) > 0:
        sqs_response["batchItemFailures"] = batch_failures

    print(f"Function ending. Response={sqs_response}")
    return sqs_response