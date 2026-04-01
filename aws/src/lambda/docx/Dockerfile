# Python version
ARG PYTHON_VERSION=3.11

# Define custom function directory
ARG FUNCTION_DIR="/function"

FROM python:${PYTHON_VERSION} AS build-image

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Create a non-root user for building
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy function code
RUN  mkdir -p ${FUNCTION_DIR}
COPY transcribe_to_docx.py ${FUNCTION_DIR}

# Install the function's dependencies
COPY requirements.txt  .
RUN  pip install --target ${FUNCTION_DIR} awslambdaric
RUN  pip install -r requirements.txt --target ${FUNCTION_DIR}

# Change ownership of the function directory to the non-root user
RUN chown -R appuser:appuser ${FUNCTION_DIR}

# Use AWS Lambda base image for the runtime stage
FROM public.ecr.aws/lambda/python:${PYTHON_VERSION}

# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${LAMBDA_TASK_ROOT}

CMD [ "transcribe_to_docx.lambda_handler" ]
