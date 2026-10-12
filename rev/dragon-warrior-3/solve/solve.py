order = [5, 2, 14, 1, 9, 7, 0, 12, 4, 15, 6, 3, 10, 8, 13, 11]
target = [104, 92, 124, 72, 116, 115, 83, 140, 100, 134, 122, 89, 112, 113, 116, 102]

transformed = [0] * 16
for i in range(16):
    transformed[order[i]] = target[i]

answer = []
for i in range(16):
    original = ((transformed[i] - (i * 3)) & 0xff) ^ 0x37
    answer.append(chr(original))

print(''.join(answer))
