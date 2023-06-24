import sqlite3
import asyncio

database = sqlite3.connect("bot.db")
cursor = database.cursor()

data = cursor.execute("select count(*) from sqlite_master where type='table' and name='users'")
for row in data:
	if row[0] == 0:
		cursor.execute('CREATE TABLE users(id INTEGER, name VARCHAR, phone_number VARCHAR, telegramID VARCHAR)')
		database.commit()

def add_user(message):
	cursor.execute("SELECT id FROM users WHERE id=?",(message.chat.id,))
	user = cursor.fetchone()
	if not user:
		cursor.execute("INSERT INTO users VALUES(?,?,?,?)",(message.chat.id,"name","phone_number","telegramID",))
		database.commit()
	else:
		return False

def drop_user_reg(user_id):
	cursor.execute("DELETE FROM users WHERE id=?",(user_id,))
	database.commit()

def add_user_name(message):
	cursor.execute("UPDATE users SET name=? WHERE id=?",(message.text,message.chat.id))
	database.commit()	

def add_user_telegramID(message):
	cursor.execute("UPDATE users SET telegramID=? WHERE id=?",(message.text,message.chat.id))
	database.commit()	

def add_user_numb(message):
	cursor.execute("UPDATE users SET phone_number=? WHERE id=?",(message.text,message.chat.id))
	database.commit()	

def get_user_name(user_id):
	cursor.execute("SELECT name FROM users WHERE id=?",(user_id,))
	user_name = cursor.fetchone()[0]
	return user_name
def get_user_numb(user_id):
	cursor.execute("SELECT phone_number FROM users WHERE id=?",(user_id,))
	user_numb = cursor.fetchone()[0]
	return user_numb
def get_user_tgID(user_id):
	cursor.execute("SELECT telegramID FROM users WHERE id=?",(user_id,))
	user_tgID = cursor.fetchone()[0]
	return user_tgID

data = cursor.execute("select count(*) from sqlite_master where type='table' and name='orders'")
for row in data:
	if row[0] == 0:
		cursor.execute('CREATE TABLE orders(id INTEGER, filial VARCHAR, order_text VARCHAR, order_time VARCHAR, order_status INTEGER, sending_time timestamp)')
		database.commit()

def create_order(message):
	cursor.execute("SELECT id FROM orders WHERE id=?",(message.chat.id,))
	order = cursor.fetchone()
	if not order:
		cursor.execute("INSERT INTO orders VALUES(?,?,?,?,?,?)",(message.chat.id,"filial","order_text","order_time","order_status","sending_time"))
		database.commit()
	else:
		return False

def choise_filial(message,filial):
	cursor.execute("UPDATE orders SET filial=? WHERE id=?",(filial,message.chat.id))
	database.commit()	

def add_order(message, order):	
	cursor.execute("UPDATE orders SET order_text=? WHERE id=?",(order,message.chat.id))
	database.commit()

def add_time(message, time):	
	cursor.execute("UPDATE orders SET order_time=? WHERE id=?",(time,message.chat.id))
	database.commit()	

def status_order(message,status):
	cursor.execute("UPDATE orders SET order_status=? WHERE id=?",(status,message.chat.id))
	database.commit()	

def sending_time(message, sending_time):
	cursor.execute("UPDATE orders SET sending_time=? WHERE id=?",(sending_time,message.chat.id))
	database.commit()

def get_filial(user_id):
	cursor.execute("SELECT filial FROM orders WHERE id=?",(user_id,))
	order_filial = cursor.fetchone()[0]
	return order_filial

def get_order_text(user_id):
	cursor.execute("SELECT order_text FROM orders WHERE id=?",(user_id,))
	order_text = cursor.fetchone()[0]
	return order_text

def get_time(user_id):
	cursor.execute("SELECT order_time FROM orders WHERE id=?",(user_id,))
	order_time = cursor.fetchone()[0]
	return order_time


async def check_order_status(chat_id, bot):
    previous_status = None  # Предыдущий статус заказа
    while True:
        cursor.execute("SELECT order_status FROM orders WHERE id=?", (chat_id,))
        order_status = cursor.fetchone()[0]
        if previous_status is None or order_status != previous_status:
            # Отправляем сообщение в чат с соответствующим статусом заказа
            if order_status == -1:
                await bot.send_message(chat_id, "Заказ приготовить не удалось")
            elif order_status == 2:
                await bot.send_message(chat_id, "Заказ принят в работу")
            elif order_status == 3:
                await bot.send_message(chat_id, "Заказ готов")

        previous_status = order_status  # Обновляем предыдущий статус

        await asyncio.sleep(5)

