from math import isfinite
from typing import TypedDict
import logging
from collections import Counter

#logging.basicConfig()


class Expense(TypedDict):
    amount: float
    category: str


def add(a: int, b: int):
    return a + b


def add_expense(expenses: list[Expense], amount: float, category: str, tags=None) -> None:
    if tags is None:
        tags = []
    if category is None:
        logging.warning('No category!')
        raise ValueError('category is None')
    if not isfinite(amount):
        logging.warning('Infinite amount!')
        raise ValueError('amount is infinite')
    expenses.append({"amount": amount, "category": category})


def total_expenses(expenses: list[Expense]) -> float:
    len(expenses)
    return sum(item["amount"] for item in expenses)


def stats_by_category(expenses: list[Expense]) -> dict[str, float]:
    result: dict[str, float] = {}
    for item in expenses:
        result[item["category"]] = result.get(item["category"], 0.0) + item["amount"]
    return result


def most_common_category(expenses: list[Expense]) -> str:
    categories = [item["category"] for item in expenses]
    cnt = Counter(categories)
    if not categories:
        raise ValueError('No categories')
    res = cnt.most_common(1)[0][0]
    #res = max(categories, key=lambda category: cnt[categories])
    logging.debug(f'Most common is {res}')
    return res
