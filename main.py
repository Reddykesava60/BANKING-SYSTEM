import json
import os
import random
import time

# --- Account Class ---
# The Account class represents a single bank account with its own data and behavior.
# It encapsulates the account number, name, and balance.
class Account:
    """
        account_number (str): A unique identifier for the account.
        name (str): The name of the account holder.
        balance (float): The current balance of the account.
    """
    def __init__(self, account_number, name, balance=0.0):
        self.account_number = account_number
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        """Deposits a specified amount into the account."""
        if amount > 0:
            self.balance += amount
            return True
        else:
            print("❌ Deposit amount must be positive.")
            return False

    def withdraw(self, amount):
        """Withdraws a specified amount from the account."""
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return False
        if amount > self.balance:
            print("❌ Insufficient funds.")
            return False
        
        self.balance -= amount
        return True

    def get_balance(self):
        """Returns the current balance of the account."""
        return self.balance

    def to_dict(self):
        """Converts the account object to a dictionary for JSON serialization."""
        return {
            "account_number": self.account_number,
            "name": self.name,
            "balance": self.balance
        }
    
    @staticmethod
    def from_dict(data):
        """Creates an Account object from a dictionary."""
        return Account(
            data["account_number"],
            data["name"],
            data["balance"]
        )

# --- Bank Class ---
# The Bank class manages all accounts, including loading, saving, and performing operations.
# It acts as the main controller for the banking system.
class Bank:
    """
    Manages the collection of bank accounts.
    
    Attributes:
        accounts (dict): A dictionary to store Account objects,
                         with account numbers as keys.
        file_name (str): The name of the file used for data persistence.
    """
    def __init__(self, file_name='accounts.json'):
        self.accounts = {}
        self.file_name = file_name
        self.load_data()

    def generate_account_number(self):
        """Generates a unique, 8-digit account number."""
        while True:
            account_number = str(random.randint(10000000, 99999999))
            if account_number not in self.accounts:
                return account_number

    def load_data(self):
        """Loads account data from the JSON file."""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    data = json.load(f)
                    for acc_data in data:
                        account = Account.from_dict(acc_data)
                        self.accounts[account.account_number] = account
                print("✅ Account data loaded successfully.")
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"⚠️ Error loading data: {e}. Starting with no accounts.")
        else:
            print("No existing account data file found. Starting a new session.")
    
    def save_data(self):
        """Saves all account data to the JSON file."""
        data = [acc.to_dict() for acc in self.accounts.values()]
        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=4)
        print("✅ Account data saved successfully.")

    def create_account(self, name):
        """Creates a new account and adds it to the bank."""
        account_number = self.generate_account_number()
        new_account = Account(account_number, name)
        self.accounts[account_number] = new_account
        self.save_data()
        print(f"\n🎉 Account created successfully for {name}!")
        print(f"Your new account number is: {account_number}")
    
    def find_account(self, account_number):
        """Finds and returns an account object by its number."""
        return self.accounts.get(account_number)

    def deposit(self, account_number, amount):
        """Performs a deposit operation on a specified account."""
        account = self.find_account(account_number)
        if account:
            if account.deposit(amount):
                self.save_data()
                print(f"✅ Successfully deposited ${amount:.2f} to account {account_number}.")
        else:
            print("❌ Account not found.")

    def withdraw(self, account_number, amount):
        """Performs a withdrawal operation on a specified account."""
        account = self.find_account(account_number)
        if account:
            if account.withdraw(amount):
                self.save_data()
                print(f"✅ Successfully withdrew ${amount:.2f} from account {account_number}.")
        else:
            print("❌ Account not found.")

    def check_balance(self, account_number):
        """Displays the balance of a specified account."""
        account = self.find_account(account_number)
        if account:
            print(f"\n📈 Account Number: {account.account_number}")
            print(f"Holder Name: {account.name}")
            print(f"Current Balance: ${account.get_balance():.2f}")
        else:
            print("❌ Account not found.")

# --- Main Application Loop ---
# This is the main function that runs the console-based user interface.
def main():
    """Main function to run the banking system console application."""
    bank = Bank()
    
    print("\n" + "="*40)
    print("      Python Console Banking System")
    print("="*40)

    while True:
        print("\nMain Menu:")
        print("1. Create New Account")
        print("2. Deposit Funds")
        print("3. Withdraw Funds")
        print("4. Check Balance")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            name = input("Enter account holder's name: ").strip()
            if name:
                bank.create_account(name)
            else:
                print("❌ Name cannot be empty.")

        elif choice == '2':
            account_number = input("Enter account number: ").strip()
            try:
                amount = float(input("Enter amount to deposit: "))
                bank.deposit(account_number, amount)
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == '3':
            account_number = input("Enter account number: ").strip()
            try:
                amount = float(input("Enter amount to withdraw: "))
                bank.withdraw(account_number, amount)
            except ValueError:
                print("❌ Invalid amount. Please enter a number.")

        elif choice == '4':
            account_number = input("Enter account number: ").strip()
            bank.check_balance(account_number)
            
        elif choice == '5':
            print("Thank you for using the banking system. Goodbye!")
            time.sleep(1)
            break
        
        else:
            print("❌ Invalid choice. Please select a number from 1 to 5.")

# Entry point of the script
if __name__ == "__main__":
    main()
