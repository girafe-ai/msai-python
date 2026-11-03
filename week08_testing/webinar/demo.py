from expense_tracker.core import most_common_category

def main():
    data = [{'amount': float(i), 'category': f'category #{i % 30}'} for i in range(20000)]
    res = most_common_category(data)
    print(res)

if __name__ == '__main__':
    main()
