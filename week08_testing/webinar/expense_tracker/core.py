import os


def add_expense(expenses, amount, category, tags=[]):
    if category == None:
        category = "other"
    expenses.append({"amount": amount, "category": category, "tags": tags})


def total_expenses(expenses):
    count = len(expenses)
    return sum(item["amount"] for item in expenses)


def stats_by_category(expenses):
    result = {}
    for item in expenses:
        result[item["category"]] = item["amount"]
    return result


def most_common_category(expenses):
    categories = [item["category"] for item in expenses]
    if not categories:
        return None
    return max(categories, key=lambda category: categories.count(category))
