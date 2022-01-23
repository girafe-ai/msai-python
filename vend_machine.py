class VENDMACHINE():

    def __init__(self, init_state):
        self.shelves = init_state['shelves']
        self.account = init_state['account']
        self.height = len(self.shelves)
        self.width = len(self.shelves[0])
        self.customer_account = init_state['customer_account']

    def put_in(self, name: str, price: float, qty: int, x: int, y: int) -> bool:
        if (y > self.height - 1) or (x > self.width - 1):
            return False

        if self.shelves[y][x] is None:
            item = {'name': name, 'price': price, 'qty': qty}
            self.shelves[y][x] = item
            return True
        else:
            return False

    def purchase(self, x: int, y: int) -> bool:

        if (y > self.height - 1) or (x > self.width - 1):  # if wrong x and y
            print(f'wrong {x=}, {y=}')
            return False

        if self.shelves[y][x] is None:  # if selected box is empty
            print(f'box {x=},{y=} empty')
            return False

        if self.customer_account['cash_now'] < self.shelves[y][x]['price']:  # if not enought money
            print('not enoght money')
            return False

        self.customer_account['cash_now'] -= self.shelves[y][x]['price']
        self.shelves[y][x]['qty'] -= 1

        if self.shelves[y][x]['qty'] == 0:
            self.shelves[y][x] = None

    def add_money(self, cash_sum: float) -> float:
        # print(f'putting ${cash_sum} money')
        self.customer_account['cash_now'] += cash_sum
        return self.customer_account['cash_now']

    def take_moneyback(self) -> float:
        self.customer_account['cash_now'] = 0
        return True

    def showcase(self):
        for shelf in self.shelves:
            shelf_view_1 = ''
            shelf_view_2 = ''
            shelf_view_3 = ''

            for box in shelf:
                if box is not None:
                    item = box.get('name')
                    price = '$' + str(box.get('price'))
                    qty = str(box.get('qty'))
                    info = price + ': x' + qty
                    separator = '|------------'
                else:
                    item = 'none'
                    info = ''
                shelf_view_1 += f'  |  {item: <10}'
                shelf_view_2 += f'  |  {info: <10}'
                shelf_view_3 += f'  {separator:<10}'

            print(shelf_view_1 + '|')
            print(shelf_view_2 + '|')
            print(shelf_view_3 + '|')
        print(f'\nCustomer cash: ${self.customer_account["cash_now"]}')

if __name__ == '__main__':
    vending_machine = {

        'shelves': [[{'name': 'candy', 'price': 10, 'qty': 3},
                     {'name': 'bread', 'price': 8, 'qty': 5},
                     {'name': 'pepsi', 'price': 20, 'qty': 6},
                     {'name': 'milk', 'price': 7, 'qty': 4}],
                    [None, None, None, None],
                    [None, None, None, None]],
        'account': {'total_sum': 1000.10, 'coins': {1: 10, 5: 15, 10: 23, 50: 12}},
        'customer_account': {'state': 'selecting',
                             'cash_now': 15,
                             'choice': {'x': None, 'y': None}}

    }
    print('----\nHere is our Vending Machine\n\n')
    VM = VENDMACHINE(vending_machine)
    VM.showcase() # show initial state

    print('----\nAdding money\n')
    VM.add_money(3.5)
    VM.showcase()

    print('----\nPutting items inside\n')
    VM.put_in('bread', 3, 2, 1, 1)
    VM.showcase()

    print('----\nDo purchase\n')
    VM.purchase(1,1)
    VM.showcase()

    print('----\nGet money back\n')
    VM.take_moneyback()
    VM.showcase()
