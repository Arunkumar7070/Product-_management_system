from flask import *
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('product_home_page.html')

@app.route('/view_products')
def view_products():
    conn = sqlite3.connect('Database/order.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return render_template('view_products.html', products=products)

@app.route('/add_product')
def add_product():
    return render_template('add_product.html')


@app.route('/add_product_into_db', methods=['POST'])
def add_product_into_db():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        conn = sqlite3.connect('Database/order.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        conn.commit()
        conn.close()
        return "Product added successfully!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)