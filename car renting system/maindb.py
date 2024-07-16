from helper import *

def main():
    while True:
        print("""
        **************************************************
        Welcome to Rent-A-Car! How can we help?
        **************************************************
        1. Rent a car
        2. Return an already rented car
        3. View available cars
        4. Exit
        **************************************************
        """)
        
        choice = int(input("Enter your choice: "))

        if choice == 1:
            cust_id = generate_cust_id() + 1
            number_of_cars = int(input("\nHow many cars would you like to rent?\n"))
            carType = int(input("\nEnter the car type (1: Sedan, 2: SUV, 3: Convertible, 4: Minivan):\n"))
            rentType = int(input("\nEnter the rent type (1: Hourly, 2: Daily, 3: Weekly):\n"))
            rent_car(cust_id, number_of_cars, carType, rentType)
        elif choice == 2:
            return_car()
        elif choice == 3:
            show_available_cars()
        elif choice == 4:
            print("Thank you for using Rent-A-Car. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
