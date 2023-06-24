from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import tracemalloc
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, InputMediaPhoto
from db import add_user, add_user_name, add_user_numb, add_user_telegramID, get_user_name, get_user_numb, get_user_tgID, drop_user_reg, create_order, choise_filial, add_order, add_time, status_order, get_filial, get_order_text, get_time, check_order_status, sending_time
from markup import inl_FL, inl_NV, contuine, inl_time, inl_itog
import json
import datetime




TOKEN = '5842358572:AAGOl88qgoRjyOLi4fbSB90XOqVGYVz47RU'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot,storage=MemoryStorage())

# Включение tracemalloc
tracemalloc.start()

messages = []

class user_reg(StatesGroup):
	name = State()
	phone_number = State()
	telegramID = State()

class SomeState(StatesGroup):
	ADD_POSITION = State()

@dp.message_handler(state=user_reg.name)
async def add_name_(message: types.Message, state=FSMContext):
	chat_id = message.chat.id
	await state.finish()
	add_user_name(message)
	await bot.send_message(chat_id, "Введите ваш ник: ")
	await user_reg.telegramID.set()

@dp.message_handler(state=user_reg.telegramID)
async def add_TGID_(message: types.Message, state=FSMContext):
	chat_id = message.chat.id
	await state.finish()
	add_user_telegramID(message)
	await bot.send_message(chat_id, "Введите ваш номер телефона: ")
	await user_reg.phone_number.set()

@dp.message_handler(state=user_reg.phone_number)
async def add_numb_(message: types.Message, state=FSMContext):
	chat_id = message.chat.id
	await state.finish()
	add_user_numb(message)
	await bot.send_message(chat_id, "Регистрация успешно завершена! \nДля оформления заказа воспользуйтесь командой /order")	

@dp.callback_query_handler(lambda call: call.data and call.data.startswith('FL'))
async def filial_callback(call, state=FSMContext):

	if call.message:
		if call.data == 'FL1':
			await bot.send_message(call.message.chat.id,'Вы выбрали филиал 1')	
			choise_filial(call.message, 'Филиал 1')
			await NV(call.message)
		if call.data == 'FL2':
			await bot.send_message(call.message.chat.id,'Вы выбрали филиал 2')
			choise_filial(call.message, 'Филиал 2')
			await NV(call.message)
		if call.data == 'FL3':
			await bot.send_message(call.message.chat.id,'Вы выбрали филиал 3')
			choise_filial(call.message, 'Филиал 3')
			await NV(call.message)

@dp.callback_query_handler(lambda call: call.data and call.data.startswith('NV'))
async def NV_callback(call, state=FSMContext):
	
	filial = get_filial(call.message.chat.id)

	if call.message:
			if call.data == 'NV_menu':
				await bot.send_message(call.message.chat.id,'Вы можете ознакомиться с меню ниже')
				if filial == 'Филиал 1':
					photo = open('C:/Users/Даша/telegram_bot/chat_bot/FL1.jpg', 'rb')
					await call.message.answer_photo(photo, caption="Меню филиала 1")
				if filial == 'Филиал 2':
					photo = open('C:/Users/Даша/telegram_bot/chat_bot/FL2.jpg', 'rb')
					await call.message.answer_photo(photo, caption="Меню филиала 2")
				if filial == 'Филиал 3':
					photo = open('C:/Users/Даша/telegram_bot/chat_bot/FL3.jpg', 'rb')
					await call.message.answer_photo(photo, caption="Меню филиала 3")	
			if call.data == 'NV_order':
				await bot.send_message(call.message.chat.id,'Вы будете возвращены к выбору филиала')
				await command_order(call.message)
			if call.data == 'NV_write_order':
				await bot.send_message(call.message.chat.id,'Вы выбрали оформить заказ')
				await order_text(call.message)
	

@dp.callback_query_handler(lambda call: call.data and call.data.startswith('min'))
async def time_callback(call, state=FSMContext):

	if call.message:

		if call.data == 'min_tyt':
			await bot.send_message(call.message.chat.id, 'Вы выбрали "Уже тут"')
			add_time(call.message, 'Уже тут')
			await itog (call.message)
		if call.data == 'min_5':
			await bot.send_message(call.message.chat.id, 'Вы выбрали "Буду через 5 минут"')
			add_time(call.message, '5 минут')
			await itog (call.message)
		if call.data == 'min_10':
			await bot.send_message(call.message.chat.id, 'Вы выбрали "Буду через 10 минут"')
			add_time(call.message, '10 минут')
			await itog (call.message)
		if call.data == 'min_20':
			await bot.send_message(call.message.chat.id, 'Вы выбрали "Буду через 20 минут"')
			add_time(call.message, '20 минут')
			await itog (call.message)
		if call.data == 'min_back':
			await NV(call.message)	


	
@dp.callback_query_handler(lambda call: call.data and call.data.startswith('itog'))
async def order_callback(call, state=FSMContext):
	if call.message:

		if call.data == 'itog_back':
			await NV(call.message)
		if call.data == 'itog_con':
			await bot.send_message(call.message.chat.id, 'Ваш заказ отправили бариста, скоро его примут в работу!')
			current_time = datetime.datetime.now()
			formatted_time = current_time.strftime("%H:%M:%S")  # Форматируем текущее время в чч:мм:сс
			sending_time(call.message,formatted_time)
			status_order(call.message,'1')

@dp.message_handler(commands='order')
async def command_order(message: types.Message, state=FSMContext):
	create_order(message)
	await message.reply("Для оформления заказа выберите один из филиалов, представленных ниже:", reply_markup=inl_FL())

async def NV(message: types.Message, state=FSMContext):
	await message.reply("Вы можете ознакомиться с меню, нажав на кнопку 📋Показать меню, представленую ниже. \nЕсли хотите выбрать другой филила, нажмите кнопку 🔙Вернуться назад. \nЕсли вы готовы сделать заказ, то нажмите кнопку 📝Оформить заказ.", reply_markup=inl_NV())
async def order_text(message: types.Message, state=FSMContext):
	await message.reply("Для оформления заказа нажмите кнопку 'Добавить позицию' и введите свой заказ ОДНИМ сообщением, если в заказе несколько позиций, отправьте их РАЗНЫМИ сообщениями. \nКоличество позиций в одном предзаказе - 20! \nПосле отправки предзаказа нажмите кнопку продолжить.", reply_markup=contuine())
	
async def time_order(message: types.Message, state=FSMContext):
	await message.reply("Выберите время посещения кофейни:", reply_markup=inl_time())
async def itog(message: types.Message):
	chat_id = message.chat.id
	filial = get_filial(chat_id)
	order_json = get_order_text(chat_id)
	order_list = json.loads(order_json)
	OTime = get_time(chat_id)

	order_lines = '\n'.join(order_list)  # Соединяем элементы списка order_list с помощью символа новой строки
    
	await message.reply("Вы выбрали {}.\nВаш заказ {}.\nВы будете через {}.\nВсе верно?".format(filial, order_lines, OTime), reply_markup=inl_itog())
	
	await check_order_status(chat_id, bot)



@dp.message_handler(lambda message: message.text == "Добавить позицию", content_types=types.ContentTypes.TEXT)
async def add_position(message: types.Message):
    await message.reply("Введите сообщение для добавления в массив:")
    await SomeState.ADD_POSITION.set()


@dp.message_handler(state=SomeState.ADD_POSITION, content_types=types.ContentTypes.TEXT)
async def process_position(message: types.Message, state: FSMContext):
    global messages
    message_text = message.text

    if len(messages) >= 20:
        await message.reply("Вы превысили количество позиций в предзаказе.")
    else:
        messages.append(message_text)  # Добавляем сообщение в массив

    await message.reply("Позиция добавлена. Если хотите добавить еще одну позицию, нажмите кнопку 'Добавить позицию'. Если хотите перейти к следующему шагу, нажмите 'Продолжить'.", reply_markup=contuine())
    await state.finish()

@dp.message_handler(lambda message: message.text=="Продолжить")
async def handle_continue(message: types.Message, state: FSMContext):
    await message.reply("Вы нажали кнопку 'Продолжить'")
    await history(message, state)


async def history(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if messages:
        await message.reply("Ваш заказ:", reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(chat_id, '\n'.join(messages))
        json_data = json.dumps(messages)
        add_order(message, json_data)
        await time_order(message)
    else:
        await bot.send_message(chat_id, 'Вы не записали ни одной позиции')
        await NV(message)     


@dp.message_handler(commands='restart')
async def command_restart(message: types.Message, state=FSMContext):
	chat_id = message.chat.id
	drop_user_reg(chat_id)
	await bot.send_message(chat_id, "Ваша запись о пользователи удалена! \nДля регистрации воспользуйтесь командой /start")


@dp.message_handler(commands='start')
async def command_start(message: types.Message, state=FSMContext):
	chat_id = message.chat.id
	user_status = add_user(message)
	if user_status == False:
		user_name = get_user_name(chat_id)
		user_numb = get_user_numb(chat_id)
		user_tgID = get_user_tgID(chat_id)
		await bot.send_message(chat_id, "Привет! \nВаше имя: {} \nВаш ник: {} \nВаш номер: {} \nДля удаления своей учетной записи воспользуйтесь командой /restart \nДля оформления заказа воспользуйтесь командой /order".format(user_name,user_tgID,user_numb))
	else:
		await bot.send_message(chat_id, 'Привет, Я бот для оформления заказов! \nДля продолжения нужно зарегестироваться \nВведи свое имя:')
		await user_reg.name.set()


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
	# Остановка tracemalloc
	tracemalloc.stop()