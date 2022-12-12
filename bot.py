import asyncio
from aiogram import Bot, Dispatcher, executor, types
from loguru import logger
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
disp = Dispatcher(bot)

@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hi there!")

if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)

