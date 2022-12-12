from aiogram import Bot, Dispatcher, executor, types, md
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from games_getter import get_curr_free, get_upcoming_free


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
    await message.reply(f"Вот что раздают бесплатно в EGS в данный момент:")
    games = get_curr_free()
    for game in games:
        await message.answer_photo(
            photo=game["keyImages"][0]["url"],
            caption=md.text(
                md.bold(f"{game['title']}"),
                md.italic(f"{game['seller']['name']}"),
                f"{int(game['price']['totalPrice']['originalPrice'])/100:.2f} "
                f"{game['price']['totalPrice']['currencyCode']}",
                sep='\n'
            ),
            parse_mode="Markdown"
        )
#TODO Доделать дату

@disp.message_handler(lambda message: message.text == "Что раздадут следующим?")
async def current_giveaway(message: types.Message):
    await message.reply(f"Вот что раздадут бесплатно в EGS в ближайшее время:")
    games = get_upcoming_free()
    for game in games:
        await message.answer_photo(
            photo=game["keyImages"][0]["url"],
            caption=md.text(
                md.bold(f"{game['title']}"),
                md.italic(f"{game['seller']['name'] if not 'Epic Dev Test Account' else 'Неизвестно'}"),
                f"{int(game['price']['totalPrice']['originalPrice']) / 100:.2f} "
                f"{game['price']['totalPrice']['currencyCode']}",
                sep='\n'
            ),
            parse_mode="Markdown"
        )


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)

