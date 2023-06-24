from datetime import datetime


from flask import Flask, redirect, render_template, request, jsonify
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bootstrap = Bootstrap4(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Даша/telegram_bot/chat_bot/bot.db'

db = SQLAlchemy(app)


@app.route("/")
def index():
    #with db.engine.connect() as conn:
        #query = text('SELECT * FROM orders WHERE order_status != 0')
        #result = conn.execute(query)
        #data = result.fetchall()
    return render_template('index.html')

@app.route('/get_buttons_from_db')
def get_buttons_from_db():
    with db.engine.connect() as conn:
        query = text('SELECT id, filial, order_text, order_time, order_status, sending_time FROM orders WHERE order_status > 0 AND order_status < 3')
        result = conn.execute(query)
        orders = []
        for row in result.fetchall():
            order = {
                'id': row[0],
                'filial': row[1],
                'order_text': row[2],
                'order_time': row[3],
                'order_status': row[4],
                'sending_time': row[5]
            }
            orders.append(order)
    return jsonify(orders=orders)

@app.route('/get_data_from_db')
def get_data_from_db():
    order_status = request.args.get('order_status')

    with db.engine.connect() as conn:
        order_query = text('SELECT id, filial, order_text, order_time, order_status, sending_time FROM orders WHERE order_status = :status')
        order_result = conn.execute(order_query, {'status': order_status})
        order_data = order_result.fetchone()

        if order_data is not None:  # Проверка наличия данных в order_data
            user_query = text('SELECT id, name, phone_number, telegramID FROM users WHERE id = :id')
            user_result = conn.execute(user_query, {'id': order_data[0]})
            user_data = user_result.fetchone()

            if user_data is not None:  # Проверка наличия данных в user_data
                response_data = {
                    'order': {
                        'id': order_data[0],
                        'filial': order_data[1],
                        'order_text': order_data[2],
                        'order_time': order_data[3],
                        'order_status': order_data[4],
                        'sending_time': order_data[5]
                    },
                    'user': {
                        'id': user_data[0],
                        'name': user_data[1],
                        'phone_number': user_data[2],
                        'IDtelegram': user_data[3]
                    }
                }
                return jsonify(data=response_data)
        
    return jsonify(data=None)

 


@app.route('/update_order_status', methods=['POST'])
def update_order_status():
    order_id = request.form.get('order_id')
    status = request.form.get('status')

    print('Order ID:', order_id)  # Проверка значения order_id
    print('Status:', status)  # Проверка значения status

    with db.engine.connect() as conn:
        # Создание объекта запроса
        query = text("UPDATE orders SET order_status=:status WHERE id=:order_id")
        
        # Выполнение запроса с передачей параметров
        conn.execute(query, {"status": status, "order_id": order_id})
        conn.commit()

    return 'Order status updated successfully'






@app.route("/FL1")
def FL1():
    return render_template("FL1.html", h1 = "CoffeeTime")

@app.route("/FL2")
def FL2():
    return render_template("FL2.html", h1 = "CoffeeTime")

@app.route("/FL3")
def FL3():
    return render_template("FL3.html", h1 = "CoffeeTime")    

if __name__ == "__main__":
    app.run(debug=True)


    #return render_template("index.html", h1 = "CoffeeTime")