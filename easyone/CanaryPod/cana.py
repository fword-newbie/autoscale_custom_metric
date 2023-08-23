import csv
import time
import subprocess
import requests
import ast
from flask import Flask, request, jsonify

# 發送指標
while True:
    query_post="query=django_http_requests_total_by_method_total{method=\"POST\"}"
    result1 = subprocess.run(['sh', 'pro.sh',query_post], capture_output=True, text=True)
    result1 = ast.literal_eval(result1.stdout)
    time.sleep(30)
    result2 = subprocess.run(['sh', 'pro.sh',query_post], capture_output=True, text=True)
    result2 = ast.literal_eval(result2.stdout)
    postv1=round(float(result1['data']['result'][0]['value'][1]),0)
    postv2=round(float(result2['data']['result'][0]['value'][1]),0)
    post_value=(postv2-postv1)/3
    if post_value<0:
        continue
    # 完成後發送到timeseries
    url = 'http://10.20.1.11:5000/predict' #timeseries predict url
    data = {'post_value': post_value}
    requests.post(url, json=data)