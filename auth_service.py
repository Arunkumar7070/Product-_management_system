from flask import *
import sqlite3


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = sqlite3.connect('Database/order.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()
        return redirect(url_for('login_page'))

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('Database/order.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            return render_template('home.html', username=user[1])
        else:
            return "Invalid credentials"

if __name__ == '__main__':
    app.run(debug=True,port=5000)