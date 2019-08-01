matrix = []

with open('in.txt', 'r') as f:
    for line in f:
        matrix.append("".join([x+"000" for x in line])[:200])
        matrix.append("0"*200)
        matrix.append("0"*200)
        matrix.append("0"*200)

print(len(matrix))
matrix = matrix[:200]

print(len(matrix[0]))
print(len(matrix))

with open('out.txt', 'wt') as f:
    for line in matrix:
        f.write(line+"\n")
