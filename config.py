from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


BOT_TOKEN = '************'
admin_id = *************

POSTGRES_URI = f"postgresql://postgres:*********@127.0.0.1:5432/rests_base"

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)



