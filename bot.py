from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
disp = Dispatcher(bot)

@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    base_kb = ReplyKeyboardMarkup(
        [[KeyboardButton("Что раздают сейчас?"), KeyboardButton("Что раздадут следующим?")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    await message.answer("Hi there!", reply_markup=base_kb)


@disp.message_handler(lambda message: message.text == "Что раздают сейчас?")
async def current_giveaway(message: types.Message):
    await message.reply(f"Вот что раздают бесплатно в EGS в данный момент:\n"
                        f"-///-")\


@disp.message_handler(lambda message: message.text == "Что раздадут следующим?")
async def current_giveaway(message: types.Message):
    await message.reply(f"Вот что раздадут бесплатно в EGS в ближайшее время:\n"
                        f"-///-")


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)

