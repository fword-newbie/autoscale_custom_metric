import matplotlib.pyplot as plt
import pandas as pd

df_tryt = pd.read_csv('/home/k8s-master/local-pv/merged.csv', names=['time','post_value','cpu'])
pv=df_tryt['post_value']
cpu=df_tryt['cpu']
npv=[0]
ncpu=[cpu[1]]
time=[0]

for i in range(2,len(pv)):
    npv.append(int(pv[i]))
    # ncpu.append(int(cpu[i])-int(cpu[i-1]))
    ncpu.append(int(cpu[i]))
    time.append((i-1)*10)

fig, ax1 = plt.subplots()

# 繪製參數 a 的折線圖
color = 'tab:red'
ax1.set_xlabel('Time C')
ax1.set_ylabel('post', color=color)
ax1.plot(time, npv, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# 創建第二個縱軸
ax2 = ax1.twinx()

# 繪製參數 b 的折線圖
color = 'tab:blue'
ax2.set_ylabel('cpu', color=color)
ax2.plot(time, ncpu, color=color)
ax2.tick_params(axis='y', labelcolor=color)

# 添加標題
plt.title('Parameter a and Parameter b over Time C')


plt.savefig('output.png', dpi=300)