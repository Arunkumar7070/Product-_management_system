from flask import *
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('place_order.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    user_id = request.form['user_id']
    product_id = request.form['product_id']
    quantity = request.form['quantity']
    conn = sqlite3.connect('Database/order.db')
    c = conn.cursor()
    c.execute("SELECT quantity FROM products WHERE id=?", (product_id,))
    result = c.fetchone()
    if not result or result[0] < int(quantity):
        conn.close()
        return "Not enough stock or invalid product."
    # Insert the order into the orders table
    c.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",(user_id, product_id, quantity))
    # Update the product quantity
    c.execute("UPDATE products SET quantity = quantity - ? WHERE id = ?",(quantity, product_id))
    conn.commit()
    conn.close()
    return "Order placed successfully!"


#using Joint query to fetch data from multiple tables
"""
@app.route('/view_orders')
def view_orders():
    conn = sqlite3.connect('Database/order.db')
    c = conn.cursor()
    c.execute('''
        SELECT o.id, u.username, p.name, o.quantity
        FROM orders o
        JOIN users u ON o.user_id = u.id
        JOIN products p ON o.product_id = p.id
    ''')
    orders = c.fetchall()
    conn.close()
    return render_template('view_orders.html', orders=orders)
"""

#using dctonary query to fetch data from multiple tables
@app.route('/view_orders')
def view_orders():
    conn = sqlite3.connect('Database/order.db')
    c = conn.cursor()

    # Retrieve orders
    c.execute('SELECT * FROM orders')
    orders = c.fetchall()

    # Retrieve users
    c.execute('SELECT * FROM users')
    users = c.fetchall()

    # Retrieve products
    c.execute('SELECT * FROM products')
    products = c.fetchall()

    conn.close()
    # Create dictionaries for users and products
    users_dict = {user[0]: user[1] for user in users}  # user_id -> username
    products_dict = {product[0]: product[1] for product in products}  # product_id -> product_name
    orders_with_details = []
    for order in orders:
        user_name = users_dict.get(order[1])  # Get username for the user_id
        product_name = products_dict.get(order[2])  # Get product name for the product_id
        orders_with_details.append({
            'order_id': order[0],
            'user_name': user_name,
            'product_name': product_name,
            'quantity': order[3]
        })
    return render_template('view_orders.html', orders=orders_with_details)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
