from flask import Flask, request, jsonify
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# 讀取CSV檔案
data_pro = pd.read_csv('/home/k8s-master/local-pv/pro.csv')  # 第一個自變量
data_vpa = pd.read_csv('/home/k8s-master/local-pv/vpa.csv')   # 應變量

# 將三個CSV檔合併成一個DataFrame
data = pd.concat([data_pro, data_vpa], axis=1)
# 分割自變量和應變量
X = data['post_value'].values
for i in range(len(X)-1,0,-1):
    X[i]=X[i]-X[i-1]
X[0]=0
y = data['cpu'].values

#切分數據為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 創建線性回歸模型並進行訓練
model = LinearRegression()
model.fit(X_train.reshape(-1, 1), y_train)

# 新
new_data = pd.DataFrame([392])
prediction = model.predict(new_data)
print(prediction)

# # 創建Flask應用程式
# app = Flask(__name__)

# # 定義API端點，處理POST請求
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # 獲取請求中的JSON數據
#         data = request.get_json()
#         new_X1_value = data['X1']
#         new_X2_value = data['X2']

#         # 使用模型進行預測
#         new_data = pd.DataFrame({'X1': [new_X1_value], 'X2': [new_X2_value]})
#         prediction = model.predict(new_data)

#         # 將預測結果以JSON格式返回
#         return jsonify({'prediction': prediction[0]})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# # 啟動Flask應用程式
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
