data = []
with open('out.txt', 'r') as fin:
    for line in fin:
        data.append(line.strip())

accuracy = eval(data[9].split(' ')[-1].split('"')[1])

with open('information.txt', 'r') as fin:
    info = fin.readlines()[0].split(' ')

name = info[0]

gender = info[1]
if gender == '男':
    gender_name = '先生'
else: gender_name = '女士'

location = info[2]

vx = info[3]

if accuracy > 90:
    say = '非常不错 加油!'
elif accuracy > 80:
    say = '很优秀 加油!'
elif accuracy > 70:
    say = '不错 加油!'
elif accuracy > 60:
    say = '还需要继续努力 加油!'
else:
    say = '不是很好 继续加油!'

print(f'你好，来自{location}的{name}{gender_name},你的语音收入了“种子计划“! 你的分数是{accuracy}!\n{say}')

