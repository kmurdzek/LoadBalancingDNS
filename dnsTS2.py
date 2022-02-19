dns = {}
with open("PROJ2-DNSTS2.txt", "r") as f:
    for line in f:
        delimed = line.split()
        dns[delimed[0]] = (delimed[1], delimed[2])
print(dns)