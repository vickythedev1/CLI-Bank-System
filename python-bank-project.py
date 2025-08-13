

import time
import pwinput
from datetime import datetime, timedelta

users = {}
suspended_users = {}
admin_password = "admin123"
secondary_admin_password = "revealpass"

def pause():
    input("\nPress Enter to continue...")

def register():
    username = input("Create a username: ")
    if username in users:
        print("Username already exists!")
        return
    password = pwinput.pwinput("Create a password: ", mask="*")
    pin = pwinput.pwinput("Set a 4-digit PIN: ", mask="*")
    users[username] = {
        "password": password,
        "pin": pin,
        "balance": 100,
        "transactions": ["Welcome bonus ₦100"],
        "logs": [],
        "suspended_until": None,
        "email": "",
        "rewards": []
    }
    print(f"✅ Account created successfully! Welcome, {username.title()}.")


def login():

    username = input("Enter username: ")
    if not users:
        print("❌ No user data found!")
        return None
    if username in users:
        if is_suspended(username):
            return None
        password = pwinput.pwinput("Enter password: ", mask="*")
        if users[username]['password'] == password:
            users[username]['logs'].append(f"Logged in at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"✅ Login successful! Welcome back, {username.title()}.")
            return username
        else:
            print("❌ Incorrect Password.")
    else:
        print("❌ User not found.")
    return None

def is_suspended(username):
    until = users[username]['suspended_until']
    if until and datetime.now() < until:
        print(f"🚫 Account suspended until {until.strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    return False

def check_balance(username):
    print(f"💼 Your current balance is: ₦{users[username]['balance']}")

def deposit(username):
    try:
        amount = float(input("Enter amount to deposit: ₦"))
        if amount > 0:
            users[username]['balance'] += amount
            users[username]['transactions'].append(f"Deposited ₦{amount}")
            print(f"✅ ₦{amount} deposited successfully!")
        else:
            print("❌ Enter a valid amount.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")

def withdraw(username):
    try:
        pin = pwinput.pwinput("Enter your PIN: ", mask="*")
        if pin != users[username]['pin']:
            print("❌ Incorrect PIN!")
            return
        amount = float(input("Enter amount to withdraw: ₦"))
        if amount > 0 and users[username]['balance'] >= amount:
            users[username]['balance'] -= amount
            users[username]['transactions'].append(f"Withdrew ₦{amount}")
            print(f"✅ ₦{amount} withdrawn successfully!")
        else:
            print("❌ Insufficient funds or invalid amount.")
    except ValueError:
        print("❌ Invalid input. Please enter a number.")

def transfer(sender):
    receiver = input("Enter recipient's username: ")
    if receiver not in users or receiver == sender:
        print("❌ Invalid recipient.")
        return
    try:
        amount = float(input("Enter amount to transfer: ₦"))
        if amount > 0 and users[sender]['balance'] >= amount:
            users[sender]['balance'] -= amount
            users[receiver]['balance'] += amount
            users[sender]['transactions'].append(f"Sent ₦{amount} to {receiver}")
            users[receiver]['transactions'].append(f"Received ₦{amount} from {sender}")
            print(f"✅ ₦{amount} sent to {receiver.title()} successfully!")
        else:
            print("❌ Invalid amount or insufficient funds.")
    except ValueError:
        print("❌ Invalid input. Enter a number.")

def transaction_history(username):
    print("\n📜 Transaction History:")
    for t in users[username]['transactions']:
        print("-", t)

def delete_account(username):
    confirm = input("Are you sure you want to delete your account? (yes/no): ")
    if confirm.lower() == "yes":
        del users[username]
        print("🗑️ Account deleted successfully!")
        return True
    else:
        print("Cancelled.")
        return False

def admin_panel():
    pwd = pwinput.pwinput("Enter admin password: ", mask="*")
    if pwd != admin_password:
        print("❌ Incorrect admin password.")
        return

    while True:
        print("\n📊 ADMIN PANEL")
        print("1. View all users")
        print("2. Suspend user")
        print("3. Unsuspend user")
        print("4. View user password")
        print("5. View user logs")
        print("6. Reset user password")
        print("7. Delete user")
        print("8. Back to main menu")
        choice = input("Choose (1-8): ")

        if choice == "1":
            for user, info in users.items():
                print(f"- {user}: ₦{info['balance']}")
        elif choice == "2":
            user = input("Username to suspend: ")
            if user in users:
                minutes = int(input("Suspend for how many minutes?: "))
                users[user]['suspended_until'] = datetime.now() + timedelta(minutes=minutes)
                print(f"🔒 {user} suspended for {minutes} minutes.")
            else:
                print("User not found.")
        elif choice == "3":
            user = input("Username to unsuspend: ")
            if user in users:
                users[user]['suspended_until'] = None
                print(f"✅ {user} unsuspended.")
        elif choice == "4":
            user = input("Username to view password: ")
            if user in users:
                second = pwinput.pwinput("Enter secondary admin password: ", mask="*")
                if second == secondary_admin_password:
                    print(f"🔐 {user}'s password: {users[user]['password']}")
                else:
                    print("❌ Incorrect secondary password.")
        elif choice == "5":
            user = input("Username to view logs: ")
            if user in users:
                for log in users[user]['logs']:
                    print("-", log)
        elif choice == "6":
            user = input("Username to reset password: ")
            if user in users:
                new_pass = pwinput.pwinput("Enter new password: ", mask="*")
                users[user]['password'] = new_pass
                print("✅ Password reset.")
        elif choice == "7":
            user = input("Username to delete: ")
            if user in users:
                del users[user]
                print("🗑️ User deleted.")
        elif choice == "8":
            break
        else:
            print("❌ Invalid option.")
        pause()

# Bank Menu
def bank_menu(username):
    while True:
        print(f"\n🏦 Welcome, {username.title()}")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Delete Account")
        print("7. Logout")
        choice = input("Select option (1-7): ")

        if choice == "1":
            check_balance(username)
        elif choice == "2":
            deposit(username)
        elif choice == "3":
            withdraw(username)
        elif choice == "4":
            transfer(username)
        elif choice == "5":
            transaction_history(username)
        elif choice == "6":
            if delete_account(username):
                break
        elif choice == "7":
            print("Logging out...")
            for i in range(3, 0, -1):
                time.sleep(1)
                print(i)
            break
        else:
            print("❌ Invalid choice!")