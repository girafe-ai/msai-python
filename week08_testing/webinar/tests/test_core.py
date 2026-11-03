import pytest

from expense_tracker.core import add_expense, total_expenses, stats_by_category, most_common_category, add

@pytest.fixture
def test_expenses():
    return [
        {"amount": 100.0, "category": "coffee"},
        {"amount": 150.0, "category": "coffee"},
        {"amount": 200.0, "category": "taxi"},
    ]

def test_total_expenses(test_expenses):
    total = total_expenses(test_expenses)
    assert total == 100.0 + 150.0 + 200.0

def test_stats_by_category(test_expenses):
    stats = stats_by_category(test_expenses)
    assert stats == {'coffee': 250.0, 'taxi': 200.0}

@pytest.mark.parametrize(("expense", "category"), [
    (10, None),
    (float('inf'), 'a')
])
def test_bad_input(expense, category):
    with pytest.raises(ValueError):
        add_expense([], expense, category)

def test_common_category(test_expenses):
    most_common = most_common_category(test_expenses)
    assert most_common == 'coffee'

def test_add1():
    assert add(1, 2) == 3

def test_add2():
    assert add('a', 'b') == 'ab'
