import pymysql.cursors

# Database connection details
DB_HOST = "localhost"
DB_USER = "burajekeith"
DB_PASSWORD = "12345678"
DB_NAME = "rentacar"

# Execute any SQL query and return results
def query_from_database(query, fetch=True):
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            if fetch:
                result = cursor.fetchall()
            else:
                result = None
            connection.commit()
    finally:
        connection.close()

    return result

# Function to get number of available cars
def show_available_cars():
    result = query_from_database("SELECT * FROM carStore")
    output = [(i["car_id"], i["carType"], i["available_cars"]) for i in result]
    for op in output:
        print(op)

# Function to generate customer id
def generate_cust_id():
    result = query_from_database("SELECT COUNT(*) as count FROM Customer")
    return result[0]["count"]

# Validate number of cars requested
def valid_car_count(n, carType):
    if n <= 0:
        print("\nPlease enter a valid car number\n")
        return False

    query = f"SELECT available_cars FROM carStore WHERE car_id = {carType}"
    result = query_from_database(query)[0]["available_cars"]

    if n > result:
        print("\nThe number of cars that you requested is more than available cars.\n")
        return False
    return True

# Rent Car on any basis
def rent_car(cust_id, number_of_cars, carType, rentType):
    if valid_car_count(number_of_cars, carType):
        if rentType == 1:
            rent_hourly(cust_id, number_of_cars, carType)
        elif rentType == 2:
            rent_daily(cust_id, number_of_cars, carType)
        else:
            rent_weekly(cust_id, number_of_cars, carType)

# Rent Hourly
def rent_hourly(cust_id, number_of_cars, carType):
    hours = int(input("\nHow many hours would you like to rent the car?\n"))
    query = f"INSERT INTO Customer (cust_id, car_rented, carTypeid, rentType, rentPeriod) VALUES ({cust_id}, {number_of_cars}, {carType}, 1, {hours})"
    query_from_database(query, fetch=False)
    query_store = f"UPDATE carStore SET available_cars = available_cars - {number_of_cars}, cars_rented = cars_rented + {number_of_cars} WHERE car_id = {carType}"
    query_from_database(query_store, fetch=False)

# Rent Daily
def rent_daily(cust_id, number_of_cars, carType):
    days = int(input("\nHow many days would you like to rent the car?\n"))
    query = f"INSERT INTO Customer (cust_id, car_rented, carTypeid, rentType, rentPeriod) VALUES ({cust_id}, {number_of_cars}, {carType}, 2, {days})"
    query_from_database(query, fetch=False)
    query_store = f"UPDATE carStore SET available_cars = available_cars - {number_of_cars}, cars_rented = cars_rented + {number_of_cars} WHERE car_id = {carType}"
    query_from_database(query_store, fetch=False)

# Rent Weekly
def rent_weekly(cust_id, number_of_cars, carType):
    weeks = int(input("\nHow many weeks would you like to rent the car?\n"))
    query = f"INSERT INTO Customer (cust_id, car_rented, carTypeid, rentType, rentPeriod) VALUES ({cust_id}, {number_of_cars}, {carType}, 3, {weeks})"
    query_from_database(query, fetch=False)
    query_store = f"UPDATE carStore SET available_cars = available_cars - {number_of_cars}, cars_rented = cars_rented + {number_of_cars} WHERE car_id = {carType}"
    query_from_database(query_store, fetch=False)

# Function to find car price based on rent type
def find_car_price(price, rentType):
    if rentType == 1:
        return (((price / 3) - 2), "hourly", "hours")
    elif rentType == 3:
        return ((price * 3), "weekly", "weeks")
    else:
        return (price, "daily", "days")

# Car return back and calculate bill
def return_car():
    bill = 0
    cstid = int(input("\nEnter your unique Customer id\n"))

    validate = f"SELECT invoice FROM Customer WHERE cust_id = {cstid}"
    validater = query_from_database(validate)

    if validater[0]["invoice"] is not None:
        print("\nCustomer already exists and bill is already paid. Please enter active Customer id.")
        return return_car()

    query = f"SELECT * FROM Customer WHERE cust_id = {cstid}"
    result = query_from_database(query)

    query_store = f"SELECT carPrice FROM carStore WHERE car_id = {result[0]['carTypeid']}"
    argument = query_from_database(query_store)

    car_price, rentTypeName, noun = find_car_price(argument[0]["carPrice"], result[0]["rentType"])
    bill = car_price * result[0]["rentPeriod"] * result[0]["car_rented"]

    # Add bill to customer entry
    update_customer = f"UPDATE Customer SET invoice = {bill} WHERE cust_id = {cstid}"
    query_from_database(update_customer, fetch=False)

    # Replenish inventory
    update_store = f"UPDATE carStore SET available_cars = available_cars + {result[0]['car_rented']}, cars_rented = cars_rented - {result[0]['car_rented']} WHERE car_id = {result[0]['carTypeid']}"
    query_from_database(update_store, fetch=False)

    print(f"""
    =============================================
    Thanks a lot for using our services
    You rented {result[0]['car_rented']} cars on {rentTypeName} basis for {result[0]['rentPeriod']} {noun}
    =============================================
    The total bill is $ {bill}
    """)

