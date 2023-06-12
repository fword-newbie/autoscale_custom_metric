from flask import Flask, request
import requests
import json
import yaml
import ast

app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def send_request_to_host():
    yaml_name=request.get_json()
    yaml_name=ast.literal_eval(yaml_name.decode('utf-8'))
    name=yaml_name["yaml_file"]
    print(name)
    with open(yaml_name, 'r') as file:
        yaml_content = yaml.load_all(file,yaml.FullLoader)
        yaml_content = list(yaml_content)[0]
       
    # 將 JSON 資料轉換為字串
    json_data = json.dumps(yaml_content)
    
    # 構建請求的 URL
    url = f'http://10.20.1.11:800/endpoint'
    
    # 發送 HTTP POST 請求，傳送 JSON 資料
    requests.post(url, data=json_data)

# 執行請求

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=800)

