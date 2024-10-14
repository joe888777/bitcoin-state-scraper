import requests

def sendMessage(
    chat_id: int,
    text: str,
    token: str
):
    url = f'https://api.telegram.org/bot{token}/sendMessage';
    message = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, json=message)
    
    if response.status_code == 200:
        print('Message successfully sent to the Telegram channel!')
    else:
        print('Message sending failed. Status code:', response.status_code)
        print('Error message:', response.text)
