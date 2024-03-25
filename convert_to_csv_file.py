with open("data/acronyms.txt", "r") as file:
    content = file.readlines()
    for line in content:
        with open("data/acronyms.csv", "a") as myFile:
            myFile.write(",".join(line.split(": ", 1)))

