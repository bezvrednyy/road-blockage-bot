from os.path import join, dirname
from dotenv import dotenv_values
from telethon import TelegramClient, events

dotenv_path = join(dirname(__file__), '.env')
config = dotenv_values(dotenv_path)

client = TelegramClient('rb_user_session', config["API_ID"], config["API_HASH"])
bot = TelegramClient('rb_bot_session', config["API_ID"], config["API_HASH"]).start(bot_token=config["BOT_TOKEN"])

bot_chats_set = set()

## Почему-то не срабатывает событие ChatAction (когда пользователь запускает бота).
@bot.on(events.NewMessage(pattern='/start'))
async def handler(event):
    bot_chats_set.add(event.chat_id)
    await event.respond('command /start detected')

@client.on(events.NewMessage(chats="@roadb_12"))
async def handler(event):
    #TODO: сделать пересылку смс (если это возможно, ведь у нас разные клиенты). Или хотя бы с ссылкой на пост в офф. канале
    for chat_id in bot_chats_set:
        await bot.send_message(chat_id, event.text)

client.start()
bot.start()
client.run_until_disconnected()

#TODO: продумать хранение чатов в S3
#TODO: придумать приветственное сообщение
#TODO: также нужно хранить 3 последних смс о перекрытии в S3