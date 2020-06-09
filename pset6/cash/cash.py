from cs50 import get_float

input = get_float("Change owed: ")

while input <= 0 and type(input) != int:
    input = get_float("Change owed: ")

number = round(input * 100)

def cash(number):
    quarters = 25
    dimes = 10
    nickels = 5
    pennies = 1
    counter = 0
    while number :
        if number >= quarters:
            number -= quarters
            counter += 1
        elif number >= dimes:
            number -= dimes
            counter += 1
        elif number >= nickels:
            number -= nickels
            counter += 1
        elif number >= pennies:
            number -= pennies
            counter += 1
    print(f"{counter}")

cash(number)
