import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
import logging
load_dotenv()


WEBHOOK_HOST='https://cd91-109-191-46-16.ngrok-free.app'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '127.0.0.1'
WEBAPP_PORT = 8000

TOKEN=os.getenv('TOKEN')
logging.basicConfig(level=logging.DEBUG)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def on_startup(dispatcher: Dispatcher):
    await dispatcher.bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dispatcher: Dispatcher):
    logging.warning('Shutting down..')
    await dispatcher.bot.delete_webhook()
    logging.warning('Webhook has been deleted. Bye!')

@dp.message_handler(commands='start')
async def start(msg: types.Message):
    await msg.answer(text=f'Доброго времени суток, {msg.from_user.full_name}✌! ')

@dp.message_handler(commands='help')
async def help(msg: types.Message):
    await msg.answer(text=f'{msg.from_user.first_name}, это бот для переотправки сообщений(эхо-бот)😎')

@dp.message_handler(commands='settings')
async def settings(msg: types.Message):
    await msg.answer(text=f'Настроек пока нет.')


@dp.message_handler(content_types='text')
async def message(msg: types.Message):
    await msg.answer(msg.text)

@dp.message_handler(content_types='photo')
async def photo(msg: types.Message):
    await msg.answer_photo(msg.photo[-1].file_id)

@dp.message_handler(content_types='video')
async def video(msg: types.Message):
    await msg.answer_video(msg.video.file_id)

@dp.message_handler(content_types='audio')
async def audio(msg: types.Message):
    await msg.answer_audio(msg.audio.file_id)

@dp.message_handler(content_types='sticker')
async def sticker(msg: types.Message):
    await msg.answer_sticker(msg.sticker.file_id)

@dp.message_handler(content_types='animation')
async def animation(msg: types.Message):
    await msg.answer_animation(msg.animation.file_id)

@dp.message_handler(content_types='voice')
async def voice(msg: types.Message):
    await msg.answer_voice(msg.voice.file_id)



start_webhook(
    dispatcher=dp,
    on_startup=on_startup,
    on_shutdown=on_shutdown,
    skip_updates=True,
    webhook_path=WEBHOOK_PATH,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
)