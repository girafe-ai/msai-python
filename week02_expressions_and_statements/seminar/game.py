# 1. Imagine a number from 1 to 1000
# 2. Computer guesses if N is correct
# 3. You answer with "=", "<" or ">"
# 4. Computer asks again, etc.

a, b = -10000, 10000

while True:
    if a == b:
        print(f'Your number is {a}')
        break
    if a > b:
        print('Something wrong')
        break

    n = (a + b) // 2
    user_input = input(f'Is {n} is correct? ')

    if user_input == '=':
        print('Wow I\'ve guessed')
        break
    elif user_input == '<':
        # go left
        a, b = a, n-1
    elif user_input == '>':
        # go right
        a, b = n+1, b
    else:
        print('Don\'t understand you.')
        continue
