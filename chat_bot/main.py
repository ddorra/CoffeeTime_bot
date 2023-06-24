from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
 
API_TOKEN = '5842358572:AAGOl88qgoRjyOLi4fbSB90XOqVGYVz47RU'
 
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Филиал 1", callback_data="Fil1"),
        types.InlineKeyboardButton(text="Филиал 2", callback_data="Fil2")
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
   await message.reply("Привет!\nЯ чат-бот для оформления предзаказов!\nДля оформления заказа выберете один из представленных филиалов ниже:", reply_markup=get_keyboard())

@dp.callback_query_handler(text="Fil1")
async def f1(message: types.Message):
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_menu = types.KeyboardButton('Показать меню')
		item_time = types.KeyboardButton('Указать время')

		markup_reply.add(item_menu, item_time)
		
			
@dp.callback_query_handler(text="Fil2")
async def f2(message: types.Message):
		markup_reply = types.ReplyKeyboardMarkup(resize_keyboard = True)
		item_menu = types.KeyboardButton('Показать меню')
		item_time = types.KeyboardButton('Указать время')

		markup_reply.add(item_menu, item_time)
		

@dp.message_handler()
async def echo(message: types.Message):
   await message.answer(message.text)
 
if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)