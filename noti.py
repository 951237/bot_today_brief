# from config import TELEGRAM_TOKEN, CHAT_ID
import requests
import telegram

TELEGRAM_TOKEN = '토큰'
CHAT_ID = '아이디'
bot = telegram.Bot(token=TELEGRAM_TOKEN)

def send(t):
    bot.sendMessage(CHAT_ID, t, parse_mode=telegram.ParseMode.HTML)

