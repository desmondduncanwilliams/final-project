#!/usr/bin/env python3
"""
Personal Budget Tracker
A command-line Python program for tracking income and expenses.
Demonstrates: variables, loops, conditionals, functions, lists, dictionaries, and file handling.
"""

import json
import os
from datetime import datetime

# File to save/load budget data
DATA_FILE = "budget_data.json"

def load_data():
    """Load existing budget data from file, or return empty structure."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                # Ensure all required keys exist for backward compatibility
                if "transactions" not in data:
                    data["transactions"] = []
                if "categories" not in data:
                    data["categories"] = ["Food", "Transportation", "Entertainment", "Bills", "Other"]
                return data
        except (json.JSONDecodeError, IOError):
            print("⚠️  Could not read data file. Starting fresh.")
    return {
        "transactions": [],
        "categories": ["Food", "Transportation", "Entertainment", "Bills", "Other"]
    }

def save_data(data):
    """Save budget data to file for persistence."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except IOError:
        print("❌ Error: Could not save data to file.")
        return False

def get_valid_amount(prompt):
    """Get a valid positive number from the user."""
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("❌ Amount must be greater than 0. Please try again.")
            else:
                return round(amount, 2)
        except ValueError:
            print("❌ Invalid input. Please enter a number (e.g., 25.50).")

def get_date_input():
    """Get date from user or use today's date."""
    print("\nDate options:")
    print("  1. Use today's date")
    print("  2. Enter a custom date")
    choice = input("Choose (1-2): ").strip()
    
    if choice == "2":
        while True:
            date_str = input("Enter date (YYYY-MM-DD): ").strip()
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return date_str
            except ValueError:
                print("❌ Invalid date format. Use YYYY-MM-DD (e.g., 2026-04-27).")
    return datetime.now().strftime("%Y-%m-%d")

def add_income(data):
    """Add a new income transaction."""
    print("\n" + "="*40)
    print("        💰 ADD INCOME")
    print("="*40)
    
    description = input("Description (e.g., 'Weekly paycheck'): ").strip()
    if not description:
        description = "Income"
    
    amount = get_valid_amount("Amount: $")
    date = get_date_input()
    
    transaction = {
        "type": "income",
        "description": description,
        "amount": amount,
        "date": date,
        "category": "Income"
    }
    
    data["transactions"].append(transaction)
    save_data(data)
    
    print(f"\n✅ Income added: +${amount:.2f} - {description}")
    print(f"   Date: {date}")

def add_expense(data):
    """Add a new expense transaction."""
    print("\n" + "="*40)
    print("        💸 ADD EXPENSE")
    print("="*40)
    
    description = input("Description (e.g., 'Grocery shopping'): ").strip()
    if not description:
        description = "Expense"
    
    amount = get_valid_amount("Amount: $")
    date = get_date_input()
    
    # Show available categories
    print("\nCategories:")
    for i, cat in enumerate(data["categories"], 1):
        print(f"  {i}. {cat}")
    print(f"  {len(data['categories']) + 1}. Add new category")
    
    while True:
        choice = input(f"Select category (1-{len(data['categories']) + 1}): ").strip()
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(data["categories"]):
                category = data["categories"][choice_num - 1]
                break
            elif choice_num == len(data["categories"]) + 1:
                new_cat = input("Enter new category name: ").strip()
                if new_cat:
                    data["categories"].append(new_cat)
                    category = new_cat
                    save_data(data)
                    break
                else:
                    print("❌ Category name cannot be empty.")
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a number.")
    
    transaction = {
        "type": "expense",
        "description": description,
        "amount": amount,
        "date": date,
        "category": category
    }
    
    data["transactions"].append(transaction)
    save_data(data)
    
    print(f"\n✅ Expense added: -${amount:.2f} - {description}")
    print(f"   Category: {category} | Date: {date}")

def view_transactions(data):
    """Display all transactions in a formatted table."""
    print("\n" + "="*60)
    print("              📋 ALL TRANSACTIONS")
    print("="*60)
    
    if not data["transactions"]:
        print("\n   No transactions yet. Add some income or expenses!")
        print("="*60)
        return
    
    # Sort by date (newest first)
    sorted_transactions = sorted(data["transactions"], 
                                  key=lambda x: x["date"], 
                                  reverse=True)
    
    # Print header
    print(f"\n{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':>10} {'Description'}")
    print("-" * 60)
    
    for t in sorted_transactions:
        date = t["date"]
        t_type = t["type"].capitalize()
        category = t["category"]
        amount = t["amount"]
        desc = t["description"]
        
        # Color-code: income in green concept, expense in red concept (using symbols)
        if t["type"] == "income":
            amount_str = f"+${amount:>8.2f}"
            type_icon = "📈"
        else:
            amount_str = f"-${amount:>8.2f}"
            type_icon = "📉"
        
        print(f"{date:<12} {type_icon} {t_type:<8} {category:<15} {amount_str:<12} {desc}")
    
    print("="*60)
    print(f"Total transactions: {len(data['transactions'])}")

def view_balance(data):
    """Calculate and display current balance with summary."""
    print("\n" + "="*40)
    print("        💵 CURRENT BALANCE")
    print("="*40)
    
    total_income = 0.0
    total_expense = 0.0
    
    for t in data["transactions"]:
        if t["type"] == "income":
            total_income += t["amount"]
        else:
            total_expense += t["amount"]
    
    balance = total_income - total_expense
    
    print(f"\n  Total Income:   +${total_income:>10.2f}")
    print(f"  Total Expenses: -${total_expense:>10.2f}")
    print("  " + "-" * 28)
    
    if balance >= 0:
        print(f"  Current Balance: ${balance:>10.2f}  ✅")
    else:
        print(f"  Current Balance: ${balance:>10.2f}  ⚠️  (Over budget!)")
    
    print("="*40)

def view_category_summary(data):
    """Show spending breakdown by category."""
    print("\n" + "="*50)
    print("           📊 SPENDING BY CATEGORY")
    print("="*50)
    
    # Calculate totals per category
    category_totals = {}
    total_expenses = 0.0
    
    for t in data["transactions"]:
        if t["type"] == "expense":
            cat = t["category"]
            amount = t["amount"]
            category_totals[cat] = category_totals.get(cat, 0) + amount
            total_expenses += amount
    
    if not category_totals:
        print("\n   No expenses recorded yet!")
        print("="*50)
        return
    
    # Sort by amount (highest first)
    sorted_categories = sorted(category_totals.items(), 
                                key=lambda x: x[1], 
                                reverse=True)
    
    print(f"\n{'Category':<20} {'Amount':>12} {'% of Total':>12} {'Bar Chart'}")
    print("-" * 50)
    
    max_amount = max(category_totals.values()) if category_totals else 1
    
    for cat, amount in sorted_categories:
        percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
        # Simple bar chart using blocks
        bar_length = int((amount / max_amount) * 20)
        bar = "█" * bar_length
        print(f"{cat:<20} ${amount:>10.2f} {percentage:>10.1f}% {bar}")
    
    print("-" * 50)
    print(f"{'TOTAL EXPENSES':<20} ${total_expenses:>10.2f}")
    print("="*50)

def delete_transaction(data):
    """Allow user to delete a specific transaction."""
    if not data["transactions"]:
        print("\n❌ No transactions to delete.")
        return
    
    print("\n" + "="*60)
    print("              🗑️  DELETE TRANSACTION")
    print("="*60)
    
    # Show numbered list
    for i, t in enumerate(data["transactions"], 1):
        t_type = "📈 Income" if t["type"] == "income" else "📉 Expense"
        print(f"{i:>3}. {t['date']} | {t_type} | ${t['amount']:.2f} | {t['description']}")
    
    print("-" * 60)
    print("  0. Cancel")
    
    while True:
        try:
            choice = int(input("\nEnter number of transaction to delete: ").strip())
            if choice == 0:
                print("Cancelled.")
                return
            if 1 <= choice <= len(data["transactions"]):
                removed = data["transactions"].pop(choice - 1)
                save_data(data)
                print(f"\n✅ Deleted: {removed['description']} (${removed['amount']:.2f})")
                return
            else:
                print("❌ Invalid selection.")
        except ValueError:
            print("❌ Please enter a number.")

def search_transactions(data):
    """Search transactions by keyword or date range."""
    print("\n" + "="*40)
    print("        🔍 SEARCH TRANSACTIONS")
    print("="*40)
    
    print("Search by:")
    print("  1. Keyword in description")
    print("  2. Date range")
    print("  3. Category")
    choice = input("Choose (1-3): ").strip()
    
    results = []
    
    if choice == "1":
        keyword = input("Enter keyword: ").strip().lower()
        results = [t for t in data["transactions"] if keyword in t["description"].lower()]
    
    elif choice == "2":
        start = input("Start date (YYYY-MM-DD): ").strip()
        end = input("End date (YYYY-MM-DD): ").strip()
        results = [t for t in data["transactions"] if start <= t["date"] <= end]
    
    elif choice == "3":
        print("\nCategories:")
        for i, cat in enumerate(data["categories"], 1):
            print(f"  {i}. {cat}")
        cat_choice = input("Select category number: ").strip()
        try:
            category = data["categories"][int(cat_choice) - 1]
            results = [t for t in data["transactions"] if t.get("category") == category]
        except (ValueError, IndexError):
            print("❌ Invalid selection.")
            return
    else:
        print("❌ Invalid choice.")
        return
    
    if not results:
        print("\n   No matching transactions found.")
        return
    
    print(f"\n   Found {len(results)} matching transaction(s):")
    print("-" * 50)
    for t in sorted(results, key=lambda x: x["date"], reverse=True):
        icon = "📈" if t["type"] == "income" else "📉"
        sign = "+" if t["type"] == "income" else "-"
        print(f"{t['date']} {icon} {sign}${t['amount']:.2f} - {t['description']}")

def display_menu():
    """Display the main menu."""
    print("\n" + "="*40)
    print("      📒 PERSONAL BUDGET TRACKER")
    print("="*40)
    print("  1. 💰 Add Income")
    print("  2. 💸 Add Expense")
    print("  3. 📋 View All Transactions")
    print("  4. 💵 Check Balance")
    print("  5. 📊 View Spending by Category")
    print("  6. 🔍 Search Transactions")
    print("  7. 🗑️  Delete Transaction")
    print("  0. 🚪 Exit")
    print("="*40)

def main():
    """Main program loop."""
    print("\n" + "="*50)
    print("  Welcome to your Personal Budget Tracker!")
    print("  Your data is automatically saved to 'budget_data.json'")
    print("="*50)
    
    # Load existing data
    budget_data = load_data()
    
    # Main loop
    while True:
        display_menu()
        choice = input("Enter your choice (0-7): ").strip()
        
        if choice == "1":
            add_income(budget_data)
        elif choice == "2":
            add_expense(budget_data)
        elif choice == "3":
            view_transactions(budget_data)
        elif choice == "4":
            view_balance(budget_data)
        elif choice == "5":
            view_category_summary(budget_data)
        elif choice == "6":
            search_transactions(budget_data)
        elif choice == "7":
            delete_transaction(budget_data)
        elif choice == "0":
            print("\n" + "="*40)
            print("  Thank you for using Budget Tracker!")
            print("  Your data has been saved. Goodbye! 👋")
            print("="*40 + "\n")
            break
        else:
            print("\n❌ Invalid choice. Please enter a number from 0 to 7.")
        
        input("\nPress Enter to continue...")

# Entry point
if __name__ == "__main__":
    main()
