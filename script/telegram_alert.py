import telegram
import asyncio
from datetime import datetime


async def SendMessage(msg):
    try:
        chat_token = "6386374481:AAFMaYiwV_RgH5FPLUUX-q5vkREC1ctzbbg"
        chat_id = 1763653421
        bot = telegram.Bot(token=chat_token)

        await bot.send_message(chat_id=chat_id, text=msg)
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    asyncio.run(SendMessage(datetime.now().strftime("%Y/%m/%d %H:%M:%S")))
