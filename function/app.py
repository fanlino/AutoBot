import os
import time
import telegram
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from util import utctime_to_localtime


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
    return f"Sent message {msg}"


async def run():
    time_info = utctime_to_localtime(datetime.utcnow())
    return await SendMessage("Server is up at " + str(time_info.hour) + ":" + str(time_info.minute))


def main():
    return asyncio.run(run())


if __name__ == "__main__":
    print(main())
