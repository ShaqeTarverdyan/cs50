from sys import argv
from csv import DictReader, reader

if len(argv) < 3:
    print("Please add 3 arg`s")
    exit()

# //open dna file
with open(argv[2]) as file:
    dnaList = reader(file)
    for dnaRow in dnaList:
        # //convert dna list to string
       dna = dnaRow[0]

# take dna sequence
# // open peopleList file, and take only header
with open(argv[1]) as headerSequences:
    dnaSequences = reader(headerSequences)
    for dnaSequence in dnaSequences:
        dnaSequence.pop(0)
        break

sequences = {}

for item in dnaSequence:
   sequences[item] = 1



for key in sequences:
    l = len(key)
    tempMax = 0
    for i in range(len(dna)):
        temp = 0
        if dna[i: i + l] == key:
            while dna[i - l: i] == dna[i: i + l]:
                temp += 1
                i += l
            if temp > tempMax:
                tempMax = temp
    sequences[key] += tempMax

with open(argv[1], newline="") as peopleList:
    people = DictReader(peopleList)
    for person in people:
        match = 0
        for dna in sequences:
            if sequences[dna] == int(person[dna]):
             match += 1
        if match == len(sequences):
            print(person['name'])
            exit()

    print("No Match")

