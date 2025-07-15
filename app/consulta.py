"""
Módulo para consultar boletines judiciales y enviar alertas por Telegram.
"""

import boto3
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from unidecode import unidecode
import pytz

import mensaje

# Configuración de DynamoDB
DYNAMODB_RESOURCE = boto3.resource('dynamodb')
TABLE = DYNAMODB_RESOURCE.Table('boletin')  # type: ignore

# Constantes
BASE_URL = "http://sica.tsjmorelos2.gob.mx/boletin"
CONSULTA_URL = f"{BASE_URL}/DT/dat_consulta.php"
BOLETIN_URL = f"{BASE_URL}/boletinjudicial.php"
ZONA_HORARIA = "America/Mexico_City"
DIAS_BUSQUEDA = 26
DIAS_VALIDACION = 6
USER_AGENT = "insomnia/2023.5.8"


def consulta_boletin(distrito: int, nombre: str) -> None:
    """
    Consulta el boletín judicial para un distrito y nombre específicos.
    
    Args:
        distrito: Número del distrito judicial
        nombre: Nombre de la persona a buscar
    """
    zona_horaria_mexico = pytz.timezone(ZONA_HORARIA)
    fecha_actual = datetime.now(zona_horaria_mexico)
    fecha_inicio = fecha_actual - timedelta(days=DIAS_BUSQUEDA)

    payload = _construir_payload(distrito, fecha_inicio, fecha_actual)
    headers = _construir_headers()
    cadena_busqueda = unidecode(nombre).lower()
    
    try:
        response = requests.post(CONSULTA_URL, data=payload, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        tabla = soup.find('table')
        
        if not tabla:
            print(f"No se encontró tabla para distrito {distrito}")
            return
            
        _procesar_tabla(tabla, cadena_busqueda, payload)
        
    except requests.RequestException as e:
        print(f"Error en la consulta HTTP: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")


def _construir_payload(distrito: int, fecha_inicio: datetime, fecha_fin: datetime) -> str:
    """Construye el payload para la consulta HTTP."""
    return (
        f"opcion=area&start={fecha_inicio.strftime('%Y-%m-%d')}"
        f"&end={fecha_fin.strftime('%Y-%m-%d')}&dato=&distritos={distrito}"
    )


def _construir_headers() -> dict:
    """Construye los headers para la consulta HTTP."""
    return {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": USER_AGENT
    }


def _procesar_tabla(tabla, cadena_busqueda: str, payload: str) -> None:
    """Procesa la tabla HTML buscando coincidencias."""
    for fila in tabla.find_all('tr'):
        for celda in fila.find_all('td'):
            texto_celda = celda.get_text(separator=" ", strip=True)
            texto_normalizado = unidecode(texto_celda).lower()
            
            if cadena_busqueda in texto_normalizado:
                _procesar_celda_con_coincidencia(celda, cadena_busqueda, payload)


def _procesar_celda_con_coincidencia(celda, cadena_busqueda: str, payload: str) -> None:
    """Procesa una celda que contiene una coincidencia."""
    for parrafo in celda.find_all('p'):
        texto_parrafo = parrafo.get_text(separator=" ", strip=True)
        texto_normalizado = unidecode(texto_parrafo).lower()
        
        if cadena_busqueda in texto_normalizado:
            mensaje_texto = _construir_mensaje(parrafo, payload)
            texto_guardado = save_and_validate_record(texto_normalizado, mensaje_texto)
            
            if texto_guardado is not None:
                mensaje.sendAlert(mensaje_texto)


def _construir_mensaje(parrafo, payload: str) -> str:
    """Construye el mensaje de alerta."""
    texto_original = parrafo.get_text(separator=" ", strip=True)
    return f"{texto_original} '{BOLETIN_URL}' {payload}"


def save_and_validate_record(texto: str, mensaje_texto: str) -> str | None:
    """
    Guarda y valida un registro en DynamoDB.
    
    Args:
        texto: Texto normalizado del registro
        mensaje_texto: Mensaje completo a guardar
        
    Returns:
        str: El texto si se guardó exitosamente, None si ya existe
    """
    current_date = datetime.now()
    record_key = texto
    
    try:
        response = TABLE.get_item(Key={'RecordKey': record_key})
        
        if 'Item' in response:
            stored_timestamp = datetime.strptime(
                response['Item']['Timestamp'], 
                '%Y-%m-%d %H:%M:%S'
            )
            
            if (current_date - stored_timestamp) < timedelta(days=DIAS_VALIDACION):
                print("Registro ya existe y tiene menos de 6 días.")
                return None
            
            print("Actualizando registro antiguo.")
        else:
            print("Guardando nuevo registro.")

        TABLE.put_item(
            Item={
                'RecordKey': record_key,
                'Timestamp': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                'mensaje_texto': mensaje_texto
            }
        )
        return texto
        
    except Exception as e:
        print(f"Error al guardar en DynamoDB: {e}")
        return None


def lambda_handler(event, context):
    """
    Handler principal para AWS Lambda.
    
    Args:
        event: Evento de AWS Lambda
        context: Contexto de AWS Lambda
    """
    nombres_busqueda = [
        "Paola Samantha Dominguez Melendez",
        "Juan Amador Mojica"
    ]
    
    distritos = [1, 9]
    
    for nombre in nombres_busqueda:
        for distrito in distritos:
            consulta_boletin(distrito, nombre)


if __name__ == "__main__":
    lambda_handler(None, None)