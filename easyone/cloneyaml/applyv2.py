from flask import Flask, request
from kubernetes import client, config
import yaml
import os

app = Flask(__name__)


def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()


k8s_client = client.ApiClient()

# 定義部署 YAML 檔案的函式
def deploy_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_content = yaml.load_all(file,yaml.FullLoader)
        yaml_content = list(yaml_content)[0]
    # 部署 YAML 檔案
    api_instance = client.AppsV1Api(k8s_client)
    api_instance.create_namespaced_deployment(body=client.V1Deployment(yaml_content),namespace="default")

    return "Deployment created"

# 定義路由處理函式
@app.route('/deploy', methods=['POST'])
def deploy_handler():
    yaml_file = request.get_json()
    yaml_file = yaml_file["yaml_file"]
    if not os.path.isfile(yaml_file):
        return f"YAML file '{yaml_file}' does not exist"
    else:
        deploy_yaml(yaml_file)

if __name__ == '__main__':
    main()
    app.run(host='0.0.0.0', port=8080)