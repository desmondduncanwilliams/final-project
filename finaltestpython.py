# Personal Budget Tracker

transactions = []
balance = 0

def show_menu():
    print("\n--- Personal Budget Tracker ---")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. Check Balance")
    print("5. View Spending by Category")
    print("6. Exit")

def add_income():
    global balance
    amount = float(input("Enter income amount: $"))
    transactions.append(("Income", amount, "None"))
    balance += amount
    print("Income added.")

def add_expense():
    global balance
    amount = float(input("Enter expense amount: $"))
    category = input("Enter category (Food, Transport, Bills, etc.): ")
    transactions.append(("Expense", amount, category))
    balance -= amount
    print("Expense added.")

def view_transactions():
    print("\n--- Transactions ---")
    for t in transactions:
        print(t)

def check_balance():
    print(f"\nCurrent Balance: ${balance:.2f}")

def spending_by_category():
    categories = {}

    for t in transactions:
        if t[0] == "Expense":
            category = t[2]
            amount = t[1]

            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount

    print("\n--- Spending by Category ---")
    for key in categories:
        print(key, ":", "$" + str(categories[key]))

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
