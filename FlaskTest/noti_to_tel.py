import requests

bot_token = "8171571651:AAFZaY4yE7M2kM88p7fFUKcaoV8oOXXgyyE"
bot_id = "@testingNotification"


def send_message(message: str) -> str:



    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': bot_id,
        'text': message,
        "parse_mode":"HTML"
    }

    response = requests.post(url, data=payload)

