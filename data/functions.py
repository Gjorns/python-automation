import os
import json
import openpyxl

def update_additions(user_id):
    accounts_file = os.path.join(os.getcwd(), 'data', 'accounts.json')
    additions_file = generate_user_path(user_id, "Price File Additions.xlsx")
    nacet_path = get_nacet_path()

    # Load the accounts data
    with open(accounts_file, 'r') as f:
        accounts_data = json.load(f)

    # Find the accounts that belong to the user
    user_accounts = [account for account in accounts_data.values() if account["owner"] == user_id]

    # Check if the additions file exists
    if not os.path.exists(additions_file):
        print(f"Price File Additions for {user_id} does not exist.")
        return

    # Open the additions file
    wb = openpyxl.load_workbook(additions_file)
    sheet = wb.active

    # Get the account numbers from column A
    account_numbers = [cell.value for cell in sheet['A']]

    # Find the user's account numbers in the additions file
    user_account_numbers = [acc["ID"] for acc in user_accounts if acc["ID"] in account_numbers]

    # Print the number of product codes awaiting to be added to the user's price files
    if user_account_numbers:
        print(f"There are {len(user_account_numbers)} product codes awaiting to be added to the price files for {user_id}.")
    else:
        print(f"No product codes found for {user_id}.")


def update_price_files():
    pass

def list_all_accounts(user_id):
    filename = os.path.join(os.getcwd(), 'data', 'accounts.json')

    with open(filename, 'r') as f:
        data = json.load(f)

    user_accounts = []
    for unique_id, account in data.items():
        if account["owner"] == user_id:
            account["ID"] = unique_id
            user_accounts.append(account)

    if len(user_accounts) == 0:
        print("There are no accounts registered under your name.")
        return

    for account in user_accounts:
        print(f"{account['ID']}\t{account['name']}\t{account['vertical']}\t{account['price_file_type']}")

def create_new_price_file(owner_id):
    filename = os.path.join(os.getcwd(), 'data', 'accounts.json')

    with open(filename, 'r') as f:
        data = json.load(f)

    while True:
        unique_id = input("Enter unique ID of the price file: ")
        if unique_id == "exit":
            return
        elif unique_id in data:
            print(f"Price file with ID {unique_id} already exists. Please try again.")
            continue

        name = input("Enter name of the price file: ")
        if name == "exit":
            return
        elif any(d["name"] == name for d in data.values()):
            print(f"Price file with name {name} already exists. Please try again.")
            continue

        print("\nSelect the vertical:")
        print("1. New Build")
        print("2. Social Housing")
        print("3. Private & Domestic")
        vertical_choice = input("Enter your choice: ")
        if vertical_choice == "1":
            vertical = "New Build"
        elif vertical_choice == "2":
            vertical = "Social Housing"
        elif vertical_choice == "3":
            vertical = "Private & Domestic"
        elif vertical_choice == "exit":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

        copper_file_choice = input("Does it have copper file? (y/n): ")
        if copper_file_choice == "y":
            copper_file = True
        elif copper_file_choice == "n":
            copper_file = False
        elif copper_file_choice == "exit":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

        print("\nSelect the price file type:")
        print("1. Margin")
        print("2. SLP")
        price_file_choice = input("Enter your choice: ")
        if price_file_choice == "1":
            price_file_type = "Margin"
        elif price_file_choice == "2":
            price_file_type = "SLP"
        elif price_file_choice == "exit":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

        data[unique_id] = {"owner": owner_id, "name": name, "vertical": vertical, "copper_file": copper_file, "price_file_type": price_file_type}

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\nPrice file with ID {unique_id} and name {name} has been created.")
        break


def create_new_user():
    estimators_file = os.path.join(os.getcwd(), 'data', 'estimators.json')
    with open(estimators_file, 'r') as f:
        data = json.load(f)

    generalpaths_file = os.path.join(os.getcwd(), 'data', 'generalpaths.json')
    with open(generalpaths_file, 'r') as f:
        general_paths = json.load(f)

    while True:
        first_name = input("Enter your first name (type 'exit' to cancel): ")
        if first_name.lower() == "exit":
            break
        elif first_name == "":
            print("First name cannot be blank. Please try again.")
            continue

        last_name = input("Enter your last name (type 'exit' to cancel): ")
        if last_name.lower() == "exit":
            break
        elif last_name == "":
            print("Last name cannot be blank. Please try again.")
            continue

        unique_id = (first_name[0] + last_name[0]).upper()

        if unique_id in data:
            print(f"Account with ID {unique_id} already exists. Please try again.")
            continue
        else:
            data[unique_id] = {"first_name": first_name, "last_name": last_name}
            with open(estimators_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            # Store user's path based on their first and last name
            first_last_name = f"{first_name} {last_name}"
            user_path = os.path.join(general_paths["nacet"], "Estimators", first_last_name)
            os.makedirs(user_path, exist_ok=True)

            print(f"User {unique_id} is created.")
            break



def remove_user():
    filename = os.path.join(os.getcwd(), 'data', 'estimators.json')

    with open(filename, 'r') as f:
        data = json.load(f)

    while True:
        user_id = input("Enter user ID (type 'exit' to cancel): ")
        if user_id.lower() == "exit":
            break
        elif user_id not in data:
            print(f"User ID {user_id} not found. Please try again.")
            continue

        first_name = data[user_id]["first_name"]
        last_name = data[user_id]["last_name"]

        confirm = input(f"Are you sure you want to remove {user_id} {first_name} {last_name} from the database? (Yes/No) ")
        if confirm.lower() == "yes":
            del data[user_id]
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"User {user_id} is removed.")
            break
        elif confirm.lower() == "no":
            break
        else:
            print("Invalid choice. Please try again.")

def list_all_users():
    filename = os.path.join(os.getcwd(), 'data', 'estimators.json')

    with open(filename, 'r') as f:
        data = json.load(f)

    print("ID\t\tFirst Name\tLast Name")
    print("--------------------------------------------------")

    for user_id, user_data in data.items():
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        print(f"{user_id}\t\t{first_name}\t\t{last_name}")


def export_data():
    accounts_file = os.path.join(os.getcwd(), 'data', 'accounts.json')
    estimators_file = os.path.join(os.getcwd(), 'data', 'estimators.json')
    wb_file = os.path.join(os.getcwd(), 'data', 'exported_data.xlsx')

    if os.path.exists(wb_file):
        os.remove(wb_file)

    wb = openpyxl.Workbook()

    default_sheet = wb.active
    default_sheet.title = "accounts"

    headers = ['Unique ID', 'Owner', 'Name', 'Vertical', 'Copperfile', 'Pricefiletype']
    default_sheet.append(headers)

    with open(accounts_file, 'r') as f:
        data = json.load(f)
        for unique_id, price_file in data.items():
            row = [unique_id, price_file['owner'], price_file['name'], price_file['vertical'], price_file['copper_file'], price_file['price_file_type']]
            default_sheet.append(row)

    wb.save(wb_file)

    print(f"Data exported to {wb_file}!")

def generate_user_path(first_name, last_name):
    filename = os.path.join(os.getcwd(), 'data', 'generalpaths.json')
    with open(filename, 'r') as f:
        data = json.load(f)
        base_path = data['nacet']
    
    user_path = os.path.join(base_path, 'Estimators', f"{first_name} {last_name}")
    
    return user_path


def get_nacet_path():
    with open('generalpaths.json', 'r') as file:
        data = json.load(file)
    return data['nacet']