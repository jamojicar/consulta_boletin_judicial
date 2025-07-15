# Consulta Boletín Judicial

Sistema automatizado para consultar boletines judiciales del Tribunal Superior de Justicia de Morelos y enviar alertas por Telegram cuando se encuentran coincidencias de nombres específicos.

## 📋 Descripción

Este proyecto monitorea automáticamente los boletines judiciales publicados en el sistema SICA del TSJ Morelos, buscando menciones de nombres específicos y enviando notificaciones instantáneas a través de Telegram cuando se encuentran coincidencias.

## 🚀 Características

- **Monitoreo automático**: Consulta boletines de los últimos 26 días
- **Búsqueda inteligente**: Normaliza nombres (sin acentos) para mejorar coincidencias
- **Notificaciones en tiempo real**: Envía alertas por Telegram
- **Deduplicación**: Evita notificaciones duplicadas usando DynamoDB
- **Múltiples distritos**: Soporte para consultar diferentes distritos judiciales
- **Manejo de errores**: Gestión robusta de errores HTTP y de base de datos


## 📦 Instalación

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de AWS con acceso a DynamoDB
- Bot de Telegram configurado

### Configuración local

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd consulta_boletin_judicial
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**
   ```bash
   export AWS_ACCESS_KEY_ID="tu_access_key"
   export AWS_SECRET_ACCESS_KEY="tu_secret_key"
   export AWS_DEFAULT_REGION="sa-east-1"
   export TOKEN_TELEGRAM="tu_token_telegram"
   export CHAT_ID="tu_chat_id"
   export ENVIRONMENT="local"
   ```

### Configuración de AWS

1. **Crear tabla DynamoDB**
   ```bash
   aws dynamodb create-table \
     --table-name boletin \
     --attribute-definitions AttributeName=RecordKey,AttributeType=S \
     --key-schema AttributeName=RecordKey,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST
   ```

2. **Configurar permisos IAM**
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": [
           "dynamodb:GetItem",
           "dynamodb:PutItem"
         ],
         "Resource": "arn:aws:dynamodb:*:*:table/boletin"
       }
     ]
   }
   ```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `AWS_ACCESS_KEY_ID` | ID de acceso de AWS | `AKIA...` |
| `AWS_SECRET_ACCESS_KEY` | Clave secreta de AWS | `...` |
| `AWS_DEFAULT_REGION` | Región de AWS | `sa-east-1` |
| `TOKEN_TELEGRAM` | Token del bot de Telegram | `123456789:ABC...` |
| `CHAT_ID` | ID del chat de Telegram | `-123456789` |
| `ENVIRONMENT` | Entorno de ejecución | `local` o `production` |

### Configuración de Telegram

1. Crear un bot con [@BotFather](https://t.me/botfather)
2. Obtener el token del bot
3. Obtener el Chat ID del grupo o chat donde enviar las alertas

## 🚀 Uso

### Ejecución local

```bash
# Activar entorno virtual
source venv/bin/activate

# Ejecutar consulta
python -m app.consulta
```

### Ejecución en AWS Lambda

El código está diseñado para ejecutarse como una función Lambda de AWS. Configura un trigger (por ejemplo, EventBridge/CloudWatch Events) para ejecutar la función periódicamente.

### Personalización de búsquedas

Edita la función `lambda_handler` en `app/consulta.py` para modificar los nombres y distritos a consultar:

```python
def lambda_handler(event, context):
    nombres_busqueda = [
        "Tu Nombre Aquí",
        "Otro Nombre"
    ]
    
    distritos = [1, 9]  # Distritos judiciales a consultar
    
    for nombre in nombres_busqueda:
        for distrito in distritos:
            consulta_boletin(distrito, nombre)
```

## 📁 Estructura del Proyecto

```
consulta_boletin_judicial/
├── app/
│   ├── __init__.py
│   ├── consulta.py      # Lógica principal de consulta
│   └── mensaje.py       # Envío de alertas por Telegram
├── .vscode/
│   └── launch.json      # Configuración de depuración
├── venv/                # Entorno virtual
├── requirements.txt     # Dependencias de Python
├── .gitignore          # Archivos ignorados por Git
└── README.md           # Este archivo
```

## 🔍 Funcionamiento

1. **Consulta HTTP**: Realiza una petición POST al sistema SICA del TSJ Morelos
2. **Parseo HTML**: Utiliza BeautifulSoup para extraer información de las tablas
3. **Búsqueda de nombres**: Normaliza y busca coincidencias de nombres
4. **Deduplicación**: Verifica en DynamoDB si ya se procesó el registro
5. **Notificación**: Envía alerta por Telegram si es una nueva coincidencia



### Logs

El sistema genera logs para:
- Consultas HTTP exitosas/fallidas
- Coincidencias encontradas
- Operaciones de DynamoDB
- Errores de envío de Telegram

### Métricas sugeridas

- Número de consultas por día
- Tasa de éxito de consultas
- Número de coincidencias encontradas
- Tiempo de respuesta promedio

## 🔒 Seguridad

- **Credenciales**: Nunca committear credenciales en el código
- **Variables de entorno**: Usar variables de entorno para configuraciones sensibles
- **IAM**: Principio de menor privilegio para permisos de AWS
- **HTTPS**: Todas las comunicaciones usan HTTPS

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.


Para reportar bugs o solicitar nuevas características:

1. Crear un issue en GitHub
2. Incluir información detallada del problema
3. Adjuntar logs relevantes (sin información sensible)


**Nota**: Este sistema está diseñado para uso personal y educativo. Asegúrate de cumplir con los términos de servicio del TSJ Morelos y las leyes aplicables. 