import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем объекты бота и диспетчера
bot = Bot(token="5842358572:AAGOl88qgoRjyOLi4fbSB90XOqVGYVz47RU")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Массив для хранения сообщений
messages = []

# Определение состояний
class AddMessageState(StatesGroup):
    InputMessage = State()

# Клавиатура с кнопками
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить сообщение")],
        [KeyboardButton(text="Просмотреть историю")]
    ],
    resize_keyboard=True
)

# Обработчик команды /start
@dp.message_handler(Command("start"))
async def start(message: types.Message):
    await message.reply('Привет! Я готов записывать сообщения.', reply_markup=keyboard)

# Обработчик кнопки "Добавить сообщение"
@dp.message_handler(lambda message: message.text == "Добавить сообщение", state="*")
async def set_message_state(message: types.Message, state: FSMContext):
    await AddMessageState.InputMessage.set()
    await message.reply("Введите сообщение, которое хотите записать:")

# Обработчик текстовых сообщений для записи в массив
@dp.message_handler(state=AddMessageState.InputMessage, content_types=types.ContentTypes.TEXT)
async def add_message(message: types.Message, state: FSMContext):
    global messages
    message_text = message.text

    if len(messages) >= 20:
        await message.reply("Массив сообщений переполнен.")
    else:
        messages.append(message_text)  # Добавляем сообщение в массив

    await state.finish()  # Завершаем состояние
    await message.reply("Сообщение добавлено.", reply_markup=keyboard)

# Обработчик кнопки "Просмотреть историю"
@dp.message_handler(lambda message: message.text == "Просмотреть историю", state="*")
async def history(message: types.Message):
    chat_id = message.chat.id
    if messages:
        await bot.send_message(chat_id, '\n'.join(messages))
    else:
        await bot.send_message(chat_id, 'История сообщений пуста.')

# Запуск бота
async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())



#async with state.proxy() as data:
        #filial = data['data_callback_fil]
        #OList = data['OL']
        #OTime = data['data_callback_time']