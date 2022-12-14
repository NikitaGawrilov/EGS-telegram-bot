import aiogram
from aiogram import Bot, Dispatcher, executor, types, md
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN
from games_getter import get_curr_free, get_upcoming_free
from utils import localize_time, get_timezone_kb
from mongodb_connector import get_user, add_user, update_timezone


bot = Bot(token=BOT_TOKEN)
disp = Dispatcher(bot)
timezone_buffer = {}

@disp.message_handler(commands=['start'])
async def start(message: types.Message):
    base_kb = ReplyKeyboardMarkup(
        [[KeyboardButton("Что раздают сейчас?"), KeyboardButton("Что раздадут следующим?")],
         [KeyboardButton("Настройки")]],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    pics = dict(await message.from_user.get_profile_photos())
    add_user(user=message.from_user, pics=pics)
    await message.answer(f"Hello there, {message.from_user.first_name}!", reply_markup=base_kb)

@disp.message_handler(lambda message: message.text == "Что раздают сейчас?")
async def current_giveaway(message: types.Message):
    await message.reply(f"Вот что раздают бесплатно в EGS в данный момент:")
    games = get_curr_free()
    for game in games:
        local_timestamps = localize_time(
            game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'],
            game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'],
            message.from_user.id
        )
        await message.answer_photo(
            photo=game["keyImages"][0]["url"],
            caption=md.text(
                md.bold(f"{game['title']}"),
                md.italic(f"{game['seller']['name']}"),
                f"{int(game['price']['totalPrice']['originalPrice'])/100:.2f} "
                f"{game['price']['totalPrice']['currencyCode']}",
                f"С {local_timestamps[0]} по {local_timestamps[1]}",
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
        local_timestamps = localize_time(
            game['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['startDate'],
            game['promotions']['upcomingPromotionalOffers'][0]['promotionalOffers'][0]['endDate'],
            message.from_user.id
        )
        await message.answer_photo(
            photo=game["keyImages"][0]["url"],
            caption=md.text(
                md.bold(f"{game['title']}"),
                md.italic(f"{game['seller']['name'] if not 'Epic Dev Test Account' else 'Неизвестно'}"),
                f"{int(game['price']['totalPrice']['originalPrice']) / 100:.2f} "
                f"{game['price']['totalPrice']['currencyCode']}",
                f"С {local_timestamps[0]} по {local_timestamps[1]}",
                sep='\n'
            ),
            parse_mode="Markdown"
        )


@disp.message_handler(lambda message: message.text == "Настройки")
async def user_settings(message: types.Message):
    user = get_user(message.from_user.id)
    buttons = [
        InlineKeyboardButton(text="⌚️ Часовой пояс", callback_data="set_tz"),
        InlineKeyboardButton(text="❕ Уведомления", callback_data="set_notifications")
    ]
    settings_kb = InlineKeyboardMarkup(row_width=1)
    settings_kb.add(*buttons)
    if user:
        await message.answer(f"Настройки:", reply_markup=settings_kb)


@disp.callback_query_handler(text="set_tz")
async def set_timezone(callback: types.CallbackQuery):
    await callback.message.answer('Укажите свой часовой пояс:')
    timezone_buffer[callback.from_user.id] = 0
    await callback.message.answer('UTC+0', reply_markup=get_timezone_kb())
    await callback.answer()


@disp.callback_query_handler(Text(startswith="tz_"))
async def timezone_callbacks(callback: types.CallbackQuery):
    action = callback.data.split('_')[1]
    if action == "plus15min":
        timezone_buffer[callback.from_user.id] += 0.25
        current_value = timezone_buffer[callback.from_user.id]
        await callback.message.edit_text(f"UTC{'+' if current_value >= 0 else ''}{current_value}",
                                         reply_markup=get_timezone_kb())
    elif action == "plus30min":
        timezone_buffer[callback.from_user.id] += 0.5
        current_value = timezone_buffer[callback.from_user.id]
        await callback.message.edit_text(f"UTC{'+' if current_value >= 0 else ''}{current_value}",
                                         reply_markup=get_timezone_kb())
    elif action == "plus1h":
        timezone_buffer[callback.from_user.id] += 1
        current_value = timezone_buffer[callback.from_user.id]
        await callback.message.edit_text(f"UTC{'+' if current_value >= 0 else ''}{current_value}",
                                         reply_markup=get_timezone_kb())
    elif action == "minus15min":
        timezone_buffer[callback.from_user.id] -= 0.25
        current_value = timezone_buffer[callback.from_user.id]
        await callback.message.edit_text(f"UTC{'+' if current_value >= 0 else ''}{current_value}",
                                         reply_markup=get_timezone_kb())
    elif action == "minus30min":
        timezone_buffer[callback.from_user.id] -= 0.5
        current_value = timezone_buffer[callback.from_user.id]
        await callback.message.edit_text(f"UTC{'+' if current_value >= 0 else ''}{current_value}",
                                         reply_markup=get_timezone_kb())
    elif action == "minus1h":
        timezone_buffer[callback.from_user.id] -= 1
        current_value = timezone_buffer[callback.from_user.id]
        await callback.message.edit_text(f"UTC{'+' if current_value >= 0 else ''}{current_value}",
                                         reply_markup=get_timezone_kb())
    elif action == "done":
        current_value = timezone_buffer[callback.from_user.id]
        if update_timezone(callback.from_user.id, current_value):
            await callback.message.edit_text(f"Новый часовой пояс успешно установлен! "
                                             f"(UTC{'+' if current_value >= 0 else ''}{current_value})")
            timezone_buffer.pop(callback.from_user.id, None)
        else:
            await callback.message.edit_text("Что-то пошло не так при попытке обновить данные... \n"
                                             "Пожалуйста, попробуйте позже.")
            timezone_buffer.pop(callback.from_user.id, None)
    elif action == "abort":
        await callback.message.edit_text('Изменение часового пояса отменено!')
        timezone_buffer.pop(callback.from_user.id, None)
    await callback.answer()


@disp.callback_query_handler(text="set_notifications")
async def set_notifications(callback: types.CallbackQuery):
    await callback.message.answer("Забей...")
    await callback.answer()


if __name__ == "__main__":
    executor.start_polling(disp, skip_updates=True)

