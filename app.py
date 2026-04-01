from flask import Flask, render_template, request, redirect
import mysql.connector
import os
from urllib.parse import urlparse

app = Flask(__name__)

# ✅ Correct env variable name
db_url = os.getenv("DATABASE_URL")

# 👉 fallback (local use)
if not db_url:
    db_url = "mysql://root:JZidTEmzAxWDoOvsnKBTrThPJwTVIFBZ@interchange.proxy.rlwy.net:23681/railway"

url = urlparse(db_url)

# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path.lstrip('/'),  # ✅ safer
    port=url.port
)

cursor = db.cursor()

# 🟢 HOME
@app.route('/')
def index():
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    return render_template('index.html', customers=data)

# 🟢 INSERT
@app.route('/insert', methods=['POST'])
def insert():
    try:
        cursor.execute("SELECT MAX(id) FROM customer")
        result = cursor.fetchone()

        id = 1 if result[0] is None else result[0] + 1

        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']

        sql = "INSERT INTO customer (id, name, mobile, amount, location) VALUES (%s, %s, %s, %s, %s)"
        values = (id, name, mobile, amount, location)

        cursor.execute(sql, values)
        db.commit()

    except Exception as e:
        print("Insert Error:", e)

    return redirect('/')

# 🔴 DELETE
@app.route('/delete/<int:id>')
def delete(id):
    try:
        cursor.execute("DELETE FROM customer WHERE id=%s", (id,))
        db.commit()
    except Exception as e:
        print("Delete Error:", e)

    return redirect('/')

# 🟡 UPDATE
@app.route('/update', methods=['POST'])
def update():
    try:
        id = request.form['id']
        name = request.form['name']
        mobile = request.form['mobile']
        amount = request.form['amount']
        location = request.form['location']

        sql = "UPDATE customer SET name=%s, mobile=%s, amount=%s, location=%s WHERE id=%s"
        values = (name, mobile, amount, location, id)

        cursor.execute(sql, values)
        db.commit()

    except Exception as e:
        print("Update Error:", e)

    return redirect('/')

# 🚀 RUN
if __name__ == "__main__":
    app.run(debug=True)