import os
import time
import requests

token = os.getenv('TOKEN_TELEGRAM')
chatId = os.getenv('CHAT_ID')

def sendAlert(notification:str):        
    r = requests.post('https://api.telegram.org/bot'+token+'/sendMessage',
              data={'chat_id': chatId, 'text': notification , 'parse_mode':'HTML'})
    print(r.text)