from expense_tracker.core import add_expense, stats_by_category, total_expenses
from expense_tracker.parser import parse_command


def execute(expenses, command, amount, category):
    if command == "add":
        add_expense(expenses, amount, category)
        return "added"
    if command == "total":
        return total_expenses(expenses)
    if command == "stats":
        return stats_by_category(expenses)
    return "bye"


def main():
    expenses = []
    print("Mini Expense Tracker")
    print("Commands: add AMOUNT CATEGORY | total | stats | quit")
    while True:
        try:
            text = input("> ")
        except EOFError:
            break
        try:
            command, amount, category = parse_command(text)
            output = execute(expenses, command, amount, category)
        except:
            print("failed")
            continue
        print(output)
        if command == "quit":
            break
    return expenses


if __name__ == "__main__":
    main()
