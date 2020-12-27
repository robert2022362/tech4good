data = []
with open('out.txt', 'r') as fin:
    for line in fin:
        data.append(line.strip())
accuracy = eval(data[8].split(' ')[-1].split('"')[1])

with open('accuracy.txt', 'w') as f:
    f.write(str(accuracy))

print(f'你的语音被“种子计划“收入! 你的正确率是{accuracy}!\n')