from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection details
DB_HOST = "localhost"
DB_USER = "burajekeith96"
DB_PASSWORD = "iq?XTZr=$FHqu2."
DB_NAME = "rentacar"

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/available_cars')
def available_cars():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carStore")
    cars = cursor.fetchall()
    conn.close()
    return render_template('available_cars.html', cars=cars)

@app.route('/rent_car', methods=['GET', 'POST'])
def rent_car():
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        number_of_cars = request.form['number_of_cars']
        carType = request.form['carType']
        rentType = request.form['rentType']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Customer (car_rented, carTypeid, rentType, rentPeriod, invoice)
            VALUES (%s, %s, %s, %s, %s)
        """, (number_of_cars, carType, rentType, 1, 0))  # rentPeriod and invoice are set as examples
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('rent_car.html')

@app.route('/return_car', methods=['GET', 'POST'])
def return_car():
    if request.method == 'POST':
        cust_id = request.form['cust_id']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customer WHERE cust_id = %s", (cust_id,))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('return_car.html')

if __name__ == '__main__':
    app.run(debug=True)
