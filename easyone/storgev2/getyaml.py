from flask import Flask, request , jsonify
import json
import yaml
import subprocess
from ast import literal_eval

app = Flask(__name__)

@app.route('/endpoint', methods=['POST'])
def handle_request():
    json_data=request.get_data("data")
    json_data=literal_eval(json_data.decode('utf-8'))
    jname = json_data["metadata"]["name"]
    jname = jname+'.yaml'
    # 改名+v2
    json_data["metadata"]["name"]=json_data["metadata"]["name"]+"v2"
    yaml_data = json.dumps(json_data)
    # 儲存 YAML 檔案
    with open(jname, 'w') as file:
        file.write(yaml_data)
    
    # sh 腳本內容
    
    subprocess.run(['sh', 'script.sh', jname])

    return '請求已處理'


@app.route('/if_exist', methods=['POST'])
def if_vpa_exist():
    pname=request.get_data("data")
    pname=pname.decode('utf-8')
    output=subprocess.run(['bash', 'vpaexist.sh' , pname], capture_output=True, text=True)
    returndata = {'exist':output.stdout}
    
    return jsonify(returndata)


@app.route('/canary_p', methods=['POST'])
def canary_p():
    # 儲存 YAML 檔案
    cpu_data=request.get_data("message")
    post_data=request.get_data("post")
    with open("puyuanv2.yaml", 'r') as yamlfile:
        # 使用PyYAML庫來解析YAML數據
        data = yaml.safe_load(yamlfile)
        data['spec']['template']['spec']['containers'][0]['resources']['limits']["cpu"]=cpu_data
    with open("/local-pv/keda-sc.yaml", 'r') as yamlfile:
        # 使用PyYAML庫來解析YAML數據
        data = yaml.safe_load(yamlfile)
        data['spec']['triggers']['metadata']['threshold']=post_data
    print("ok")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=800)