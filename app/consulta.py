import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import mensaje
import pytz
from datetime import datetime, timedelta
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('boletin')

def consulta_boletin(distrito,nombre):
    zona_horaria_mexico = pytz.timezone("America/Mexico_City")
    fecha_actual = datetime.now(zona_horaria_mexico)
    fecha_menos_tres_dias = fecha_actual - timedelta(days=26)

    url = "http://sica.tsjmorelos2.gob.mx/boletin/DT/dat_consulta.php"

    payload = f"opcion=area&start={fecha_menos_tres_dias.strftime('%Y-%m-%d')}&end={fecha_actual.strftime('%Y-%m-%d')}&dato=&distritos={distrito}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "insomnia/2023.5.8"
    }   
    cadena_a_buscar = unidecode(nombre).lower()
    response = requests.request("POST", url, data=payload, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    #soup = BeautifulSoup(response.text, "html.parser").get_text(separator=" ", strip=True)
    tabla = soup.find('table')
    for fila in tabla.find_all('tr'):
        for celda in fila.find_all('td'):
            texto = celda.get_text(separator=" ", strip=True)
            texto = unidecode(texto).lower()
            posicion = texto.find(cadena_a_buscar)
            if posicion != -1:
                i = 0
                for parrafo in celda.find_all('p'):
                    texto = parrafo.get_text(separator=" ", strip=True)
                    texto = unidecode(texto).lower()
                    posicion = texto.find(cadena_a_buscar)                
                    if posicion != -1:
                        mensaje_texto = parrafo.get_text(separator=" ", strip=True)  #f"posible coincidencia '{cadena_a_buscar}' fue encontrada {posicion}"
                        mensaje_texto = f"{mensaje_texto} 'http://sica.tsjmorelos2.gob.mx/boletin/boletinjudicial.php' {payload}"
                        texto = save_and_validate_record(texto,mensaje_texto)
                        if texto != None:
                            mensaje.sendAlert(mensaje_texto)
                    i= i +1 

def save_and_validate_record(texto,mensaje_texto):
    # Extrae la fecha del registro o usa la fecha actual
    current_date = datetime.now()
    record_key = texto  # O usa una parte única de record para crear la clave primaria
    
    # Buscar el registro en DynamoDB
    response = table.get_item(Key={'RecordKey': record_key})
    
    # Si el registro existe
    if 'Item' in response:
        stored_timestamp = datetime.strptime(response['Item']['Timestamp'], '%Y-%m-%d %H:%M:%S')
        
        # Validar si el registro tiene menos de 6 días
        if (current_date - stored_timestamp) < timedelta(days=6):
            print("Registro ya existe y tiene menos de 3 días.")
            return
        
        # Si el registro es más antiguo, actualizar
        print("Actualizando registro antiguo.")
    else:
        print("Guardando nuevo registro.")

    # Guardar o actualizar el registro con la fecha actual
    table.put_item(
        Item={
            'RecordKey': record_key,
            'Timestamp': current_date.strftime('%Y-%m-%d %H:%M:%S'),
            'mensaje_texto': mensaje_texto
        }
    ) 
    return texto                                  

def lambda_handler(event, context):
    zona_horaria_mexico = pytz.timezone("America/Mexico_City")
    fecha = datetime.now(zona_horaria_mexico)
    nombre  = "Paola Samantha Dominguez Melendez"
    consulta_boletin(1,nombre)
    consulta_boletin(9,nombre)
    nombre  = "Juan Amador Mojica"
    consulta_boletin(1,nombre)
    consulta_boletin(9,nombre)
    
        


__main__ = lambda_handler(None,None)