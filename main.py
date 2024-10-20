from utils import *
from os.path import join, dirname
from dotenv import dotenv_values
from telethon import TelegramClient, events

dotenv_path = join(dirname(__file__), '.env')
config = dotenv_values(dotenv_path)

client = TelegramClient('rb_user_session', config['API_ID'], config['API_HASH'])
bot = TelegramClient('rb_bot_session', config['API_ID'], config['API_HASH']).start(bot_token=config['BOT_TOKEN'])

keywords = {'планируется перекрытие'}
monitored_chats = ["@roadb_12"]

bot_chats_set = set()

## Почему-то не срабатывает событие ChatAction (когда пользователь запускает бота).
@bot.on(events.NewMessage(pattern='/start'))
async def handler(event):
    bot_chats_set.add(event.chat_id)
    await event.respond('command /start detected')

@client.on(events.NewMessage(chats=monitored_chats))
async def handler(event):
    hasSomeKeyword = False
    strippedText = stripAll(event.text)
    message = event.message
    for keyword in keywords:
        if keyword in strippedText:
            hasSomeKeyword = True
            break
    
    if hasSomeKeyword:
        postLink = 't.me/roadb_12/' + str(message.id)
        text = event.text + ' ' + postLink

        for chat_id in bot_chats_set:
            #Пересылка сообщения возможна в рамках одного клиента, поэтому мы можем только слать от своего имени
            await bot.send_message(chat_id, text, link_preview=False)

client.start()
bot.start()
client.run_until_disconnected()

#TODO: продумать хранение чатов в S3
#TODO: придумать приветственное сообщение
#TODO: также нужно хранить 3 последних смс о перекрытии в S3