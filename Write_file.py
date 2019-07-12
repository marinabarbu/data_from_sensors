f = open("example.txt", "w+")
for i in range(1,5):
    line = input("Scrie 2 numere: ")
    f.write(line + '\n')
f.close()