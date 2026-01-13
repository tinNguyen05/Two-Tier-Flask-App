import os
import mysql.connector
import time
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Cấu hình kết nối sử dụng mysql-connector-python
def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST', '127.0.0.1'),
                user=os.environ.get('MYSQL_USER', 'root'),
                password=os.environ.get('MYSQL_PASSWORD', '1234'), # Đã cập nhật mật khẩu
                database=os.environ.get('MYSQL_DB', 'flask_db')
            )
            return conn
        except Exception as e:
            retries -= 1
            print(f"Đang đợi Database... Còn {retries} lần thử. Lỗi: {e}")
            time.sleep(3)
    return None

def init_db():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()

@app.route('/')
def index():
    conn = get_db_connection()
    messages = []
    if conn:
        cursor = conn.cursor()
        cursor.execute('SELECT message FROM messages')
        messages = cursor.fetchall() # Trả về list các tuple (message,)
        cursor.close()
        conn.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    new_message = request.form.get('new_message')
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
        conn.commit()
        cursor.close()
        conn.close()
    return jsonify({'message': new_message})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)