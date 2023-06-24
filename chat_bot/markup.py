from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def inl_FL():
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Филиал 1", callback_data="FL1"),
        types.InlineKeyboardButton(text="Филиал 2", callback_data="FL2"),
        types.InlineKeyboardButton(text="Филиал 3", callback_data="FL3"),
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

#btn_phone = KeyboardButton('Поделиться номером', request_contact=True)
#btn_TGID = KeyboardButton('Поделиться ником', request_user=True)

#inl_phone = ReplyKeyboardMarkup()
#inl_phone.add(inl_phone)
 
#inl_TGID = ReplyKeyboardMarkup()
#inl_TGID.add(inl_TGID)

def inl_NV():

	buttons = [
		types.InlineKeyboardButton(text="📋Показать меню",callback_data="NV_menu"),
		types.InlineKeyboardButton(text="🔙Вернуться назад",callback_data="NV_order"),
		types.InlineKeyboardButton(text="📝Оформить заказ",callback_data="NV_write_order")
	]

	keyboard = types.InlineKeyboardMarkup(row_width=2)
	keyboard.add(*buttons)
	return keyboard

def contuine():

	keyboard = ReplyKeyboardMarkup(
	keyboard=[
		[KeyboardButton(text="Добавить позицию")],
		[KeyboardButton(text="Продолжить")]
	],
	resize_keyboard=True
	)
	return keyboard


def inl_time():

	buttons = [
		types.InlineKeyboardButton(text="Уже тут",callback_data="min_tyt"),
		types.InlineKeyboardButton(text="Буду через 5 минут",callback_data="min_5"),
		types.InlineKeyboardButton(text="Буду через 10 минут",callback_data="min_10"),
		types.InlineKeyboardButton(text="Буду через 20 минут",callback_data="min_20"),
		types.InlineKeyboardButton(text="🔙Вернуться назад",callback_data="min_back")
	]

	keyboard = types.InlineKeyboardMarkup(row_width=2)
	keyboard.add(*buttons)
	return keyboard

def inl_itog():

	buttons = [
		types.InlineKeyboardButton(text="Все верно, отправить предзаказ",callback_data="itog_con"),
		types.InlineKeyboardButton(text="🔙Вернуться назад",callback_data="itog_back")
		]

	keyboard = types.InlineKeyboardMarkup(row_width=2)
	keyboard.add(*buttons)
	return keyboard