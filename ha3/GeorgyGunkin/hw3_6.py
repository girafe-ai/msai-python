from typing import Tuple

class Item:
    ###
    ### Stack of single type items
    ###

    EmptyItemName = "0"

    def __init__(self, name: str, cost: int):
        self.name = name

        if (name == Item.EmptyItemName):
            self.stack = 0
        else:
            self.stack = 1

        self.cost = cost

    @classmethod
    def EmptyItem(cls):
        return cls(Item.EmptyItemName, 0)

    def IsEmpty(self):
        return self.stack <= 0

    def Push(self, item: str, cost: int) -> None:

        if (self.stack > 0 and item != self.name):
            raise ValueError(f"Attempted to push {item} to stack with items of type {self.name}")
        
        self.name = item
        self.cost = cost
        self.stack += 1

    def Pop(self) -> bool:
        if (self.stack > 0):
            self.stack -= 1
            return True
        
        return False


class VendingMachine:
    def __init__(self, numShelves: int, shelfCapacity: int):
        self.numShelves = numShelves
        self.shelfCapacity = shelfCapacity
    
        self.totalPositions = numShelves * shelfCapacity

        self.storage = list()

        self.money = 0

        for i in range(numShelves):
            self.storage.append(list())

            for j in range(shelfCapacity):
                self.storage[i].append(Item.EmptyItem())
    
    def GenerateCoordinate(self, position: int) -> Tuple[int, int]:
        return divmod(position, self.shelfCapacity)

    def ValidatePosition(self, position: int) -> Tuple[int, int]:
        if (position < 0 or position >= self.totalPositions):
            raise ValueError("Position exceeded the possible range of positios for the Vending Machine")

        return self.GenerateCoordinate(position)

    def InsertItem(self, position: int, item: str, cost: int) -> None:
        shelfNum, pos = self.ValidatePosition(position)

        self.storage[shelfNum][pos].Push(item, cost)

    def PurchaseItem(self, position: int, givenMoney: int) -> None:
        shelfNum, pos = self.ValidatePosition(position)

        if (self.storage[shelfNum][pos].IsEmpty()):
            print(f"Could not make a purchase: there are no items on position {position}")
        else:
            if (givenMoney < self.storage[shelfNum][pos].cost):
                print(f"Could not make a purchase of item {self.storage[shelfNum][pos].name} on position {position}: \
                        not enough money is given ({givenMoney}) for the cost of {self.storage[shelfNum][pos].cost}")
                return

            change = givenMoney - self.storage[shelfNum][pos].cost

            if (self.money < change):
                print(f"Successfully purchased item {self.storage[shelfNum][pos].name} on position {position}. \
                        But, Could only give a change of {self.money}")
                self.money = 0
                return

            self.money += self.storage[shelfNum][pos].cost

            print(f"Successfully purchased item {self.storage[shelfNum][pos].name} on position {position}. Change = {change}")

            self.storage[shelfNum][pos].Pop()

    def AddMoney(self, amount: int) -> None:
        if (amount < 0):
            raise ValueError("Cannot add negative amount of money")

        print(f"Added money to Vending Maching. Total money = {self.money}")

        self.money += amount
    
    def TakeAllMoney(self) -> None:
        if (self.money <= 0):
            print("No money left in the machine")

        print(f"Withdrawn {self.money} in cash")

        self.money = 0

    def Print(self) -> None:
        print("Showing contents of the Vending Machine:")
        for i in range(self.numShelves):
            for j in range(self.shelfCapacity):
                if (j == self.shelfCapacity - 1):
                    end = "\n"
                else:
                    end = " "
                
                print(self.storage[i][j].name, end=end)

        print("_________________________________________")

m = VendingMachine(5, 3)

m.AddMoney(100)

m.Print()

m.InsertItem(14, "A", 5)
m.InsertItem(14, "A", 5)
m.InsertItem(7, "B", 12)

m.Print()

m.PurchaseItem(14, 5)
m.PurchaseItem(14, 5)
m.PurchaseItem(7, 13)
m.PurchaseItem(7, 13)

m.TakeAllMoney()
