import os
import telegram
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(verbose=True)

# Path to Kubernetes Secrects
token_path = "/secrets/default/telegram-secret/chat_token"
id_path = "/secrets/default/telegram-secret/chat_id"

chat_token = os.getenv('CHAT_TOKEN')
chat_id = os.getenv('CHAT_ID')

if chat_token == None or chat_id == None:
    try:
        with open(token_path, 'r') as a, open(id_path, 'r') as b:
            chat_token = a.read().rstrip('\n')
            chat_id = b.read().rstrip('\n')
            a.close()
            b.close()
    except Exception as ex:
        print(ex)
        print("Cannot read from Kubernetes Secrets")
        exit(1)

async def SendMessage(msg):
    try:
        bot = telegram.Bot(token=chat_token)

        await bot.send_message(chat_id=chat_id, text=msg)
    except Exception as ex:
        print(ex)
    return "Sent message"

def main():
    message = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    result = asyncio.run(SendMessage(message))
    return result

if __name__ == "__main__":
    print(main())
