from cs50 import get_string
from string import ascii_lowercase

text = get_string("Text: ")

letters = 0
words = 1
sentences = 0

for i in text:
    if i.isalpha() :
        letters += 1
    elif i.isspace():
        words += 1
    elif i == ".":
        sentences += 1

L = 100 * (letters / words)
S = 100 * (sentences / words)
grade = 0.0588 * L - 0.296 * S - 15.8



if grade > 16:
    print("Grade 16+")
elif grade < 1:
    print("Before Grade 1")
else:
    print(f"Grade {round(grade)}")