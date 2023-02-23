import os
import json
from data.functions import *

def price_files_menu(user_id):
    if user_id:
        print(f"\nLogged in as {user_id}\n")

    while True:
        print("\nPRICE FILES\n-----------------\n")
        print("1. Update Additions")
        print("2. Update Price Files")
        print("3. Create New Price File")
        print("4. List All Accounts")
        print("0. Back")

        choice = input("\nEnter your choice: ")
        if choice == "1":
            update_additions(user_id)
        elif choice == "2":
            update_price_files(user_id)
        elif choice == "3":
            create_new_price_file(user_id)
        elif choice == "4":
            list_all_accounts(user_id)
        elif choice == "0":
            return
        else:
            print("\nInvalid choice. Please try again.\n")

def user_management_menu():
    while True:
        print("\nUSER MANAGEMENT\n-----------------")
        print("1. Create New User")
        print("2. Remove User")
        print("3. List All Users")
        print("0. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_new_user()
        elif choice == "2":
            remove_user()
        elif choice == "3":
            list_all_users()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    filename = os.path.join(os.getcwd(), 'data', 'estimators.json')

    with open(filename, 'r') as f:
        data = json.load(f)

    user_id = None

    while True:
        print("\nMAIN MENU\n-----------------")
        print("1. Price Files")
        print("2. User Management")
        print("3. Export Data")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            while not user_id:
                user_id = input("Enter user ID: ")
                if user_id not in data:
                    print("Incorrect ID.\n")
                    user_id = None
            price_files_menu(user_id)
        elif choice == "2":
            user_management_menu()
        elif choice == "3":
            export_data()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()