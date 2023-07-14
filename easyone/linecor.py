import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# 讀取 CSV 檔案
df = pd.read_csv('/home/k8s-master/local-pv/merged.csv')

# 將時間欄位解析為日期時間格式
df['timestamp'] = pd.to_datetime(df['time'])

# 設置時間欄位為索引
df.set_index('timestamp', inplace=True)

# 分別提取兩個資料組的數據列
data_group1 = df['post_value']
data_group2 = df['cpu']

# 繪製兩個資料組的時間序列折線圖
plt.plot(data_group1.index, data_group1, label='Data Group 1')
plt.plot(data_group2.index, data_group2, label='Data Group 2')

# 添加標籤和標題
plt.xlabel('Time')
plt.ylabel('Value')
plt.title('Time Series Analysis')

# 添加圖例
plt.legend()

# 檢查兩個資料組之間的相關性
result = sm.tsa.stattools.coint(data_group1, data_group2)
p_value = result[1]

print(p_value)