from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import requests, csv
import yaml
import subprocess
import math

# 創建Flask應用程式
app = Flask(__name__)


# # 建立模型 分析完再通知
# data_pro = pd.read_csv('/home/k8s-master/local-pv/pro.csv')  # 舊的沒memory的
data_pro = pd.read_csv('/home/k8s-master/local-pv/wpro.csv')  # 第一個自變量

# CPU的模型
data = pd.concat([data_pro], axis=1)
# # 分割自變量和應變量
# X = data['post_value'].values
# for i in range(len(X)-1,0,-1):
#     X[i]=X[i]-X[i-1]
# X[0]=0
# y = data['cpu_usage'].values

# #切分數據為訓練集和測試集
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 創建線性回歸模型並進行訓練
# model = LinearRegression()
# model.fit(X_train.reshape(-1, 1), y_train)

# memory的模型
# 分割自變量和應變量
m_x = data['post_value'].values
for i in range(len(m_x)-1,0,-1):
    m_x[i]=m_x[i]-m_x[i-1]
m_x[0]=0
m_y = data['mem_usage'].values

#切分數據為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(m_x, m_y, test_size=0.3, random_state=82)

# 創建線性回歸模型並進行訓練
mem_model = LinearRegression()
mem_model.fit(X_train.reshape(-1, 1), y_train)

plt.scatter(X_test.reshape(-1, 1), y_test, color='blue', label='Post_frequency')
plt.plot(X_test.reshape(-1, 1), mem_model.predict(X_test.reshape(-1, 1)), color='green', label='Predicted Memory usage')
plt.xlabel('Post(frequency)')
plt.ylabel('Memory_usage(M)')
plt.legend()
plt.show()
plt.savefig("m.png")

# # 新
# new_data = pd.DataFrame([359])
# prediction = model.predict(new_data)
# print(prediction)


    # # 完成後發送到Canary
    # url = 'http://canary:80/' #Canary url
    # data = {'message': 'ok'}
    # requests.post(url, json=data)
# tick=1
# # 定義API端點，處理POST請求
# @app.route('/predict', methods=['POST'])
# def predict():
#     # 獲取請求中的JSON數據
#     global tick
#     data = request.get_json()
#     new_X1_value = data['post_value']
#     # 使用模型進行預測
#     new_data = pd.DataFrame([new_X1_value])
#     # prediction = model.predict(new_data)
#     # metric=int(prediction[0])
#     mem_prediction=mem_model.predict(new_data)
#     metric=int(mem_prediction[0])
#     # url = 'http://10.244.0.26:31314/predict' #Canary url
#     # data = {'message': int(prediction[0]),'post':new_X1_value}
#     # requests.post(url, json=data)
#     # 讀取TXT檔案
#     print(metric)
#     with open('/home/k8s-master/local-pv/a.txt', 'r') as file:
#         current_value = int(file.read().strip())
#     if tick % 2 == 1:
#         with open('/home/k8s-master/puyuan-v3.yaml', 'r') as file:
#             data = yaml.safe_load(file)
#     else:
#         with open('/home/k8s-master/puyuan-v2.yaml', 'r') as file:
#             data = yaml.safe_load(file)
#     print(current_value)
#     print(metric*10)
#     if (current_value*int(8)) < (metric*10):#放大資源
#         #改資源 cpu換mem
#         #data['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = (str(math.ceil(metric*1.2))+'m')
#         data['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = (str(math.ceil(metric*1.2))+'Mi')
#         with open('/home/k8s-master/local-pv/a.txt', 'w') as files:
#             files.write(str(math.ceil(metric*1.2)))

#         if  math.ceil(new_X1_value/10/20) <= 2:#最低2
#             data['spec']['replicas'] = 2
#         # elif (math.ceil(new_X1_value/10/20)) >= 10:#最高10
#         #     data['spec']['replicas']=10
#         #     with open('/home/k8s-master/puyuan-vn.yaml', 'w') as file:
#         #         yaml.dump(data, file)
#         else:
#             data['spec']['replicas']=math.ceil(new_X1_value/10/20)

#         if tick % 2 == 1:
#             data['metadata']['name']="puyuan-v2"
#             data['spec']['template']['metadata']['labels']['version']="v2"
#             data['spec']['selector']['matchLabels']['version']="v2"
#             with open('/home/k8s-master/puyuan-v2.yaml', 'w') as file:
#                 yaml.dump(data, file)
#             tick = tick + 1
#             subprocess.run(['sh', 'deploy.sh', '/home/k8s-master/puyuan-v2.yaml','puyuan-v2','/home/k8s-master/100v2.yaml', '/home/k8s-master/v3-no.yaml'])
#         else:
#             data['metadata']['name']="puyuan-v3"
#             data['spec']['template']['metadata']['labels']['version']="v3"
#             data['spec']['selector']['matchLabels']['version']="v3"
#             with open('/home/k8s-master/puyuan-v3.yaml', 'w') as file:
#                 yaml.dump(data, file)
#             tick = tick + 1
#             subprocess.run(['sh', 'deploy.sh', '/home/k8s-master/puyuan-v3.yaml','puyuan-v3', '/home/k8s-master/100v3.yaml', '/home/k8s-master/v2-no.yaml'])
#         print("big")
        
#     elif (current_value*int(3)) > (metric*10):#縮限資源
#         #改資源 卡掉cpu給memory
#         #data['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = (str(math.ceil(metric*1.2))+'m')
#         data['spec']['template']['spec']['containers'][0]['resources']['requests']['memory'] = (str(math.ceil(metric*1.2))+'Mi')
#         with open('/home/k8s-master/local-pv/a.txt', 'w') as files:
#             files.write(str(math.ceil(metric*1.2)))
#         if  math.ceil(new_X1_value/10/20) <= 2:#最低2
#             data['spec']['replicas'] = 2
#             # elif (math.ceil(new_X1_value/10/20)) >= 10:#最高10
#             #     data['spec']['replicas']=10
#             #     with open('/home/k8s-master/puyuan-vn.yaml', 'w') as file:
#             #         yaml.dump(data, file)
#         else:
#             data['spec']['replicas'] = math.ceil(new_X1_value/10/20)

#         if tick % 2 == 1:
#             data['metadata']['name']="puyuan-v2"
#             data['spec']['template']['metadata']['labels']['version']="v2"
#             data['spec']['selector']['matchLabels']['version']="v2"
#             with open('/home/k8s-master/puyuan-v2.yaml', 'w') as file:
#                 yaml.dump(data, file)
#             tick = tick + 1
#             subprocess.run(['sh', 'deploy.sh', '/home/k8s-master/puyuan-v2.yaml','puyuan-v2', '/home/k8s-master/100v2.yaml', '/home/k8s-master/v3-no.yaml'])
#         else:
#             data['metadata']['name']="puyuan-v3"
#             data['spec']['template']['metadata']['labels']['version']="v3"
#             data['spec']['selector']['matchLabels']['version']="v3"
#             with open('/home/k8s-master/puyuan-v3.yaml', 'w') as file:
#                 yaml.dump(data, file)
#             tick = tick + 1
#             subprocess.run(['sh', 'deploy.sh', '/home/k8s-master/puyuan-v3.yaml','puyuan-v3', '/home/k8s-master/100v3.yaml', '/home/k8s-master/v2-no.yaml'])
#         print("small")
#     else:
#         if data['spec']['replicas'] != math.ceil(new_X1_value/10/20):
#             if data['spec']['replicas'] >= 10:
#                 data['spec']['replicas']=10
#             elif data['spec']['replicas'] <= 2:
#                 data['spec']['replicas']=2
#             elif math.ceil(new_X1_value/10/20)>10:
#                 data['spec']['replicas']=10
#             elif math.ceil(new_X1_value/10/20)<2:
#                 data['spec']['replicas']=2
#             else:
#                 data['spec']['replicas']=math.ceil(new_X1_value/10/20)
#             print(data['spec']['replicas'])
#             print("b")
#             #觸發水平    
#             if tick % 2 == 1:
#                 with open('/home/k8s-master/puyuan-v3.yaml', 'w') as file:
#                     yaml.dump(data, file)
#                 subprocess.run(['sh', 'mywayhpa.sh', '/home/k8s-master/puyuan-v3.yaml'])
#             else:
#                 with open('/home/k8s-master/puyuan-v2.yaml', 'w') as file:
#                     yaml.dump(data, file)
#                 subprocess.run(['sh', 'mywayhpa.sh', '/home/k8s-master/puyuan-v2.yaml'])
#             print("!?") 
#         else: #屁事不幹
#             print("!")
#     print(tick)
#     return jsonify({'g': "g"})

    
#     # # 更新資料
#     # url = 'http://10.244.0.197:31314/new' #Canary url
#     # bb = {'cpu':math.ceil(metric/data['spec']['replicas']),'howm':math.ceil(new_X1_value/10/20),'dp_name':data['metadata']['name']}
#     # requests.post(url, json=bb)
#     # if data['metadata']['name'] == "puyuan-v1":
#     #     subprocess.run(['sh', 'deploy.sh',"../../100v1.yaml"])
#     # else:
#     #     subprocess.run(['sh', 'deploy.sh',"../../100v2.yaml"])     

#     # url = 'http://10.244.0.197:31314/old' #Canary url
#     # if data['metadata']['name'] == "puyuan-v1":
#     #     cc={'old':"puyuan-v2"}
#     # else:
#     #     cc={'old':"puyuan-v1"}
#     # requests.post(url, json=cc)




# # 啟動Flask應用程式
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)









# # # 替換以下參數為你的 YAML 檔案路徑和要更新的 key 和 value
# # yaml_file_path = 'your_yaml_file.yaml'
# # key_to_update = 'your_key'
# # # new_value = 'your_new_value'

# # with open('/home/k8s-master/puyuan-vn.yaml', 'r') as file:
# #     data = yaml.safe_load(file)

# # data['spec']['template']['spec']['containers'][0]['resources']['requests']['cpu'] = "10m"

# # # 將修改後的 YAML 寫回檔案
# # with open('/home/k8s-master/puyuan-vn.yaml', 'w') as file:
# #     yaml.dump(data, file)

