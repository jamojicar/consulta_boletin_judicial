# Project Structure

## Directory Organization

```
consulta_boletin_judicial/
├── app/                    # Main application code
│   ├── consulta.py        # Core consultation logic and Lambda handler
│   └── mensaje.py         # Telegram messaging functionality
├── .kiro/                 # Kiro AI assistant configuration
│   └── steering/          # AI guidance documents
├── .vscode/               # VS Code configuration
├── venv/                  # Python virtual environment (local only)
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore patterns
└── README.md             # Project documentation
```

## Module Responsibilities

### `app/consulta.py`
- **Primary module**: Contains main business logic
- **Web scraping**: HTTP requests to TSJ Morelos SICA system
- **Data processing**: HTML parsing with BeautifulSoup
- **Database operations**: DynamoDB record management
- **Lambda handler**: Entry point for AWS Lambda execution
- **Search logic**: Name normalization and matching

### `app/mensaje.py`
- **Notification service**: Telegram Bot API integration
- **Alert formatting**: Message construction and delivery
- **Environment validation**: Token and chat ID verification

## Code Organization Patterns

### Function Naming
- Use descriptive snake_case names
- Private functions prefixed with underscore (`_construir_payload`)
- Public functions use clear action verbs (`consulta_boletin`, `sendAlert`)

### Constants
- Define at module level in UPPER_CASE
- Group related constants together (URLs, timeouts, etc.)

### Error Handling
- Use try-except blocks for external service calls
- Log errors with descriptive messages
- Graceful degradation for non-critical failures

### Configuration
- Environment variables for all external dependencies
- No hardcoded credentials or sensitive data
- Clear separation between local and production configs