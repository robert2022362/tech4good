print('====== 欢迎使用“种子计划” ======')
name = input('请输入你的名字: ')
gender = input('请输入你的性别: ')
city = input('请输入你的城市: ')
vx = input('输入你的微信号: ')

with open('information.txt', 'w') as fout:
    fout.write(str(name)+' '+str(gender)+' '+str(city)+' '+str(vx))

    