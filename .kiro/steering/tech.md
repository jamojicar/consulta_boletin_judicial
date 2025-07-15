# Technology Stack

## Core Technologies
- **Python 3.8+**: Primary programming language
- **AWS Lambda**: Serverless execution environment
- **DynamoDB**: NoSQL database for deduplication and state management
- **Telegram Bot API**: Notification delivery system

## Key Dependencies
- `requests==2.31.0`: HTTP client for web scraping
- `beautifulsoup4==4.12.3`: HTML parsing and data extraction
- `unidecode==1.3.8`: Text normalization (accent removal)
- `pytz==2023.3`: Timezone handling for Mexico City timezone
- `boto3==1.35.55`: AWS SDK for DynamoDB operations

## Environment Configuration
Required environment variables:
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
- `TOKEN_TELEGRAM`, `CHAT_ID`
- `ENVIRONMENT` (local/production)

## Common Commands

### Local Development
```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m app.consulta
```

### AWS Setup
```bash
# Create DynamoDB table
aws dynamodb create-table \
  --table-name boletin \
  --attribute-definitions AttributeName=RecordKey,AttributeType=S \
  --key-schema AttributeName=RecordKey,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST
```

## Architecture Patterns
- **Serverless**: Designed for AWS Lambda with event-driven execution
- **Separation of concerns**: Distinct modules for consultation logic and messaging
- **Error handling**: Comprehensive exception handling for HTTP and database operations
- **Idempotency**: DynamoDB-based deduplication prevents duplicate alerts