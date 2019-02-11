import telepot
from config import *
import urllib3
import time
import requests

proxy_url = "http://proxy.server:3128"
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))
bot = telepot.Bot(BOT_TOKEN)

APIURL = "http://127.0.0.1:5000/api/"

def handle(message):
    """
    The Telegram Bot code for AInstein, this connects AInstein API
    to Telegram. This bot sends the message to the AInstein API sends
    its response back to the user

    Parameters
    ----------
    message : str
        The data being sent to the telegram bot

    Returns
    -------
    response : str
        The reply to be sent to the user
    """
    contentType, chatType, chatID = telepot.glance(message)
    print(contentType, chatType, chatID)
    if contentType == 'text':
        endPoint = "textback/?mode={}&query={}"
        query = message['text']
        response = requests.get(APIURL+endPoint.format('text', query)).json()
        bot.sendMessage(chatID, response['response'])

    if contentType == "voice":
            data = bot.getFile(message['voice']['file_id'])
            endPoint = "textback/?mode={}&location={}"
            response = requests.get(APIURL+endPoint.format('voice', data['file_path'])).json()
            # print(response)
            bot.sendMessage(chatID, response['response'])

bot.message_loop(handle)
print("Bot Running...")
while 1:
    time.sleep(10)