from darts import TimeSeries,explainability, utils
import pandas as pd
import datetime



# 讀取 a.csv，指定列名為 ['a', 'b']
df_a = pd.read_csv('/home/k8s-master/local-pv/pro.csv', names=['time', 'post_value'])


# 讀取 b.csv，指定列名為 ['c', 'd']
df_b = pd.read_csv('/home/k8s-master/local-pv/vpa.csv', names=['cpu'])


# 合併兩個資料框
df_merged = pd.concat([df_a, df_b], axis=1, join='inner', ignore_index=False)
df_merged.drop(labels=0,inplace=True)


# 儲存合併後的結果到新的檔案
df_merged.to_csv('/home/k8s-master/local-pv/merged.csv', index=False)

# prodata=TimeSeries.from_csv("/home/k8s-master/local-pv/merged.csv",time_col="time")
# print(prodata)
# a=utils.statistics.check_seasonality(prodata)
# print(a)

# # 計算變數間的相關性
# correlation_matrix = correlation(series_a, series_b, series_c, series_d)

# print(correlation_matrix)
