# Product Overview

## Consulta Boletín Judicial

Automated system for monitoring judicial bulletins from the Superior Court of Justice of Morelos (TSJ Morelos) and sending Telegram alerts when specific names are found.

### Core Functionality
- **Automated monitoring**: Queries bulletins from the last 26 days
- **Intelligent search**: Normalizes names (removes accents) for better matching
- **Real-time notifications**: Sends alerts via Telegram
- **Deduplication**: Prevents duplicate notifications using DynamoDB
- **Multi-district support**: Supports querying different judicial districts
- **Error handling**: Robust HTTP and database error management

### Target Environment
- Designed for AWS Lambda execution with periodic triggers
- Can also run locally for development and testing
- Uses DynamoDB for state management and Telegram for notifications

### Key Use Case
Personal/educational tool for monitoring legal proceedings by tracking specific names in judicial bulletins published by the Mexican court system.