from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Function to get a connection to the database
def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=ell887db.database.windows.net;'
        'DATABASE=productdb;'
        'UID=nidhi;'
        'PWD=ell887#cc'
    )
    return conn

    # Create a table in Azure SQL Database if not exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the table exists
    cursor.execute("SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'products'")
    if not cursor.fetchone():
        # Create the table if it doesn't exist
        cursor.execute('''CREATE TABLE products
                        (id INT PRIMARY KEY IDENTITY,
                        name NVARCHAR(255) NOT NULL,
                        description NVARCHAR(255),
                        price FLOAT)''')
        conn.commit()
    
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')


# Route to add new products
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, description, price) VALUES (?, ?, ?)', (name, description, price))
        conn.commit()
        conn.close()
        return redirect(url_for('index')) 
    return render_template('add_product.html')

# Route to list all products
@app.route('/list_products')
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    print(products)
    conn.close()
     
    return render_template('list_products.html', products=products)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
