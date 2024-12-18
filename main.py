import multiprocessing
from utils import *
from metrics import *
from os.path import join, dirname
from dotenv import dotenv_values
from telethon import TelegramClient, events

dotenv_path = join(dirname(__file__), '.env')
config = dotenv_values(dotenv_path)
keywords = {'планируется перекрытие'}
monitored_chats = ['@gibdd_rme', '@mariroads_testsource']

client = TelegramClient('rb_user_session', config['API_ID'], config['API_HASH'])

@client.on(events.NewMessage(chats=monitored_chats))
async def handler(event):
  hasSomeKeyword = False
  strippedText = stripAll(event.text)
  for keyword in keywords:
    if keyword in strippedText:
      hasSomeKeyword = True
      break
  
  if hasSomeKeyword:
      await event.message.forward_to(config['TARGET_CHANEL_ID'])


if __name__ == '__main__':
  bg_send_metrics = multiprocessing.Process(target=send_metrics)
  bg_send_metrics.start()

  client.start()
  client.run_until_disconnected()

  bg_send_metrics.terminate()