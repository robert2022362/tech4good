print('====== 欢迎使用“种子计划” ======')
name = input('请输入你的名字: ')
gender = input('1. 男    2. 女\n请选择你的性别[1/2]: ')

while gender != '1' and gender != '2':
    gender = input('请重新选择，输入1或2进行选择: ')

if gender == '1':
    gender = '男'
elif gender == '2':
    gender = '女'

city = input('请输入你的城市: ')
vx = input('输入你的微信号: ')

with open('information.txt', 'w') as fout:
    fout.write(str(name)+' '+str(gender)+' '+str(city)+' '+str(vx))

    