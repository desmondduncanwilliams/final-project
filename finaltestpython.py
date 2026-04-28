# Personal Budget Tracker
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import json
import os

console = Console()

transactions = []
balance = 0
filename = "budget_data.json"

def load_data():
    global transactions
    global balance

    if os.path.exists(filename):

        with open(filename,"r") as file:
            data = json.load(file)

            transactions = data["transactions"]
            balance = data["balance"]

def save_data ():
    data = { 
        "transactions": transactions,    
        "balance": balance
    }
    with open(filename, 'w') as file:
         json.dump (data,file)

    print ("Progress saved.")
    
        
def show_menu():
    text = """
    1. Add Income")
    2. Add Expense")
    3. View Transactions")
    4. Check Balance")
    5. View Spending by Category")
    6. Exit")
    """
    console.print(Panel(text, title="PERSONAL BUDGET TRACKER"))

def add_income():
    global balance

    amount = float(input("Enter income amount: $"))
    name = input("Enter income source:")

    transactions.append(("Income", amount, "None"))
    balance += amount

    save_data()
    text = "Money Added Successfully!\n"
    text += "Source: " + name + "\n"
    text += "Amount: $" + str(amount)
    console.print(Panel(text, title="INCOME ADDED", style="green"))
    
def add_expense():
    global balance
    amount = float(input("Enter expense amount: $"))
    category = input("Enter category (Food, Transport, Bills, etc.): ")

    transactions.append(["Expense", category, amount])
    balance -= amount

    save_data()
    text = "Expense Added Successfully!\n"
    text += "Category: " + category + "\n"
    text += "Amount: $" + str(amount)
    console.print(Panel(text, title="EXPENSE ADDED", style="red", border_style="red"))
    
def add_bill():

    global balance

    amount = float(input("Enter bill amount: $"))
    name = input("Enter bill name: ")
    transactions.append(["Bill", name, amount])
    balance = balance - amount

    save_data()
    text = "Bill Added Successfully!\n"
    text += "Bill: " + name + "\n"
    text += "Amount: $" + str(amount)
    console.print(Panel(text,title="BILL ADDED",style="blue"))

def view_transactions():
    table = Table(title="ALL TRANSACTIONS")

    table.add_column("Type")
    table.add_column("Name")
    table.add_column("Amount")

    for item in transactions:
        table.add_row(item[0],item[1],"$" + str(item[2]))
        console.print(Panel(text, title="BALANCE", style="green"))

def check_balance():
    text = "Current Balance: $" + str(balance)
    console.print(Panel(text, title="BALANCE", style="green"))

def spending_by_category():
    totals = {}

    for item in transactions:
        if item[0] == "Expense" or item[0] == "Bill":
            name = item[1]
            amount = item[2]

            if name in totals:
                    totals[name] = totals[name] + amount
            else:
                    totals[name] = amount 
    
    table = Table(title="SPENDING BY CATEGORY")
    table.add_column("Category")
    table.add_column("Total")

    for key in totals:
        table.add_row(key,"$" + str(totals[key]))

    console.print(table)

load_data()

    
# Main Program Loop
while True:
    show_menu()
    choice = input("Choose an option: ")

    if choice == "1":
        add_income()

    elif choice == "2":
        add_expense()

    elif choice == "3":
        view_transactions()

    elif choice == "4":
        check_balance()

    elif choice == "5":
        spending_by_category()

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid choice. Try again.")
