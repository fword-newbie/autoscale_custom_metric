import csv
import time
import subprocess
import requests
import ast
from flask import Flask, request, jsonify


query_post="query=sum(node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{container=\"puyuan\"})"
query_start="start="+"2023-07-26T03:04:46.000000Z"
query_end="end="+"2023-07-26T03:24:46.000000Z"

result1 = subprocess.run(['sh', 'pro.sh',query_post , query_start, query_end], capture_output=True, text=True)
result1 = ast.literal_eval(result1.stdout)
print(result1)

prd=[]
cc=len(result1['data']['result'][0]['values'])
cpu_usage=result1['data']['result'][0]['values']
for i in range(cc):
    prd.append({"cpu_usage":float(cpu_usage[i][1])})

fieldnames = ["cpu_usage"] # no get_pro
with open("/shared-data/my-cpu-use.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # 寫入欄位名稱
    writer.writerows(prd)  # 寫入資料
    
# app = Flask(__name__)

# # 發送指標
# @app.route('/', methods=['POST'])
# def send_metrics():
#     try:
#         # 解析夾帶的JSON資料
#         data = request.get_json()

#         if data is not None and "message" in data and data["message"] == "ok":
#             # # 觸發後等待10秒後執行        
#             time.sleep(10)
#             query_post="query=avg(rate(django_http_requests_total_by_method_total{method=\"POST\"}[30s]))"
#             result1 = subprocess.run(['sh', 'pro.sh',query_post], capture_output=True, text=True)
#             result1 = ast.literal_eval(result1.stdout)
#             post_value=result1['data']['result'][0]['values'][1]

#             print(post_value)
#             result = {"message": "ok"}

#             # 完成後發送到timeseries
#             url = 'http://10.20.1.11:5000/predict' #timeseries predict url
#             data = {'post_value': post_value}
#             requests.post(url, json=data)
#         else:
#             result = {"message": "not_ok"}

#         return jsonify(result)
#     except Exception as e:
#         return jsonify({"error": str(e)})
    
# 收指標然後做決策

# @app.route('/scale', methods=['POST'])
# def scale():
#     json_data = request.get_json()
#     send_metrics=float(json_data['message'])
#     post_value=float(json_data['post'])
#     csv_file_path = '/shared-data/cpu_limit.csv'  
#     with open(csv_file_path, 'r', newline='') as csvfile:
#         csv_reader = csv.reader(csvfile)
#         next(csv_reader)
#         second_row = next(csv_reader)
#     value = int(second_row[0])
#     if (value*int(7)) < send_metrics*10:
#         # url = 'http://10.20.1.11:800/canary_p' # 放大
#         # data = {'message': send_metrics,"post":post_value}
#         print(send_metrics*1.5,post_value)
#     elif (value*int(3)) > send_metrics*10:
#          # url = 'http://10.20.1.11:800/canary_p' # 縮小
#             # data = {'message': send_metrics,"post":post_value}
#             # requests.post(url, json=data)
#         print(send_metrics*0.5,post_value)
#     else: 
#         print("yes")
#     return jsonify({'n': "a"})


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=31312)


