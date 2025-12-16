# AWS Infrastructure

Terraform code to deploy the infrastructure used in ATS.

## Transcription Configuration

The transcription service is configured with the following features:

- **Language Detection**: Automatically identifies the primary language of uploaded audio files
- **Speaker Identification**: Labels different speakers in the audio (up to 10 speakers)
- **PII Redaction**: Detects and redacts personally identifiable information, generating both redacted and unredacted transcript versions

## Secret Manager Integration

Teams and Slack webhook URLs are stored securely in AWS Secrets Manager instead of directly in environment variables. 

### Configuration
When you enable Teams or Slack notifications (`teams_notification = true` or `slack_notification = true`), the system will:

1. Create a secret in AWS Secrets Manager with the webhook URL from `teams_webhook` or `slack_webhook` variables
2. Configure the Lambda functions to retrieve the webhook URL from the secret at runtime
3. If no webhook secret is configured, notifications will be disabled and logged only

### Benefits
- **Enhanced Security**: Webhook URLs are encrypted at rest in Secrets Manager
- **Access Control**: Fine-grained IAM permissions for secret access
- **Rotation Support**: Easy webhook URL updates without Lambda redeployment
- **Secure by Default**: Notifications are disabled if no secret is configured
