from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB = 'database.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
        ''')

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect(DB)
    if request.method == 'POST':
        t_type = request.form['type']
        amount = float(request.form['amount'])
        category = request.form['category']
        date = request.form['date']
        conn.execute('INSERT INTO transactions (type, amount, category, date) VALUES (?, ?, ?, ?)',
                     (t_type, amount, category, date))
        conn.commit()
        return redirect('/')
    cur = conn.execute('SELECT * FROM transactions ORDER BY date DESC')
    data = cur.fetchall()
    income = sum(row[2] for row in data if row[1] == 'Income')
    expense = sum(row[2] for row in data if row[1] == 'Expense')
    balance = income - expense
    return render_template('index.html', data=data, income=income, expense=expense, balance=balance)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
