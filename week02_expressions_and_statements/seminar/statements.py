import random

def sort1(a, b, c):
    if a < b:
        if a < c:
            if b < c:
                return a, b, c
            else:
                return a, c, b
        else:
            return c, a, b
    else:  # b <= a
        if b < c:
            if a < c:
                return b, a, c
            else:
                return b, c, a
        else:
            return c, b, a

def sort2(a, b, c):
    if a <= b <= c:  # a <= b and b <= c
        return a, b, c
    elif a <= c <= b:
        return a, c, b
    elif b <= a <= c:
        return b, a, c
    elif b <= c <= a:
        return b, c, a
    elif c <= a <= b:
        return c, a, b
    elif c <= b <= a:  # else
        return c, b, a

variants = [
    (1, 2, 3),
    (1, 3, 2),
    (2, 1, 3),
    (2, 3, 1),
    (3, 1, 2),
    (3, 2, 1),
]

for a, b, c in variants:
    answer1 = sort1(a, b, c)
    answer2 = sort2(a, b, c)
    if answer1 == (1, 2, 3) and answer2 == (1, 2, 3):
        print('success')
    else:
        print('fail')
        break
else:
    print('tests passed')


i = 0
while i < len(variants):
    a, b, c = variants[i]
    answer1 = sort1(a, b, c)
    answer2 = sort2(a, b, c)
    if answer1 == (1, 2, 3) and answer2 == (1, 2, 3):
        print('success')
    else:
        print('fail')
        break
    i += 1
else:
    print('tests passed')



def big_function(i):
    for j in range(5000000):
        i += random.randint(-1, 1)
    print(i)
    return i


a = [
    big_function(1000 ** i)
    for i in range(5)
]
b = (
    big_function(1000 ** i)
    for i in range(5)
)

print(list(a))
print(list(b))