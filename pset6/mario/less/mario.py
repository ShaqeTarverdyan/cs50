from cs50 import get_int

number = get_int("Height: ")

def mario(n):

  for i in range(0,n):

    m = n - i
    for j in range(0, m):
        print(end=" ")

    m = m - 1
    for j in range(0, i+1):
        print("#", end="")
    print("\r")


if number <= 0 or number > 8 :
    print("Number is not valid")
else :
    mario(number)


