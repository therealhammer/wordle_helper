fivechars = []

with open("german.dic", "r") as file:
    lines = file.readlines()

for line in lines:
    if len(line) == 6:
        fivechars.append(line.lower())


with open("newdict.txt", "w") as f:
    f.writelines(fivechars)