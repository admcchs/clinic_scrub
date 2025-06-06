import os
import psycopg2
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Get the DATABASE_URL environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set")

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

@app.route('/')
def home():
    return "Clinic Stock Scrub System is running!"

@app.route('/clinics')
def clinics():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT clinic_name FROM clinics;')
    clinics = cur.fetchall()
    cur.close()
    conn.close()
    clinic_list = [clinic[0] for clinic in clinics]
    return jsonify(clinic_list)

@app.route('/order', methods=['GET', 'POST'])
def order():
    conn = get_db_connection()
    cur = conn.cursor()
    # Real clinic list from DB
    cur.execute('SELECT clinic_name FROM clinics ORDER BY clinic_name;')
    clinics = [row[0] for row in cur.fetchall()]
    # Real item list
    cur.execute('SELECT item_code, description FROM items ORDER BY description;')
    items = cur.fetchall()
    cur.close()
    conn.close()

    if request.method == 'POST':
        clinic = request.form['clinic']
        item_code = request.form['item_code']
        quantity = int(request.form['quantity'])
        flash(f"Order received: {quantity} of {item_code} from {clinic}", "success")
        return redirect(url_for('order'))

    return render_template('order.html', clinics=clinics, items=items)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
