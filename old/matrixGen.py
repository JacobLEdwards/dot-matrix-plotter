import numpy as np

filename = 'testfile.txt'

array = np.ones(23)

array = [str(int(x)) for x in array]
array = "00000000".join(array)

array += "0"

matrix = []
for i in range(200):
    if i % 9 == 0:
        matrix.append(array)
    else:
        matrix.append("".join([str(x) for x in np.zeros(200, dtype=int)]))

print(len(array.replace(" ", "")))
print(len(matrix))

with open(filename, 'wt') as f:
    for line in matrix:
        f.write(line)
