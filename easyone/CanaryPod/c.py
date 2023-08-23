from kubernetes import client, config
from flask import Flask, request, jsonify

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

if __name__ == '__main__':
    main()

# 創建 Kubernetes 的 API 客戶端
apps_v1 = client.AppsV1Api()
v1 = client.CoreV1Api()

# 指定要同步調整的 Deployment 的名稱和命名空間
namespace = "default"

    # 新的副本數和資源配置

app = Flask(__name__)

@app.route('/new', methods=['POST'])
def new():
    data = request.get_json()
    cpu=data['cpu']
    howm=data['howm']
    deployment_name=data['dp_name']
    new_replicas = int(howm)
    new_resource_requests = {
        "cpu": str(cpu),
        "memory": "5mi",
    }

    # 新副本數
    deployment = apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
    deployment.spec.replicas = new_replicas
    apps_v1.replace_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)

    # 新副本資源
    pods = v1.list_namespaced_pod(namespace=namespace, label_selector=f"app={deployment_name}")
    for pod in pods.items:
        pod_name = pod.metadata.name
        pod.spec.containers[0].resources.requests = new_resource_requests
        v1.replace_namespaced_pod(name=pod_name, namespace=namespace, body=pod)
    return jsonify({'g': "g"})
    
@app.route('/old', methods=['POST'])
def old():
    data = request.get_json()
    close=data['old']
    old_resource_requests = {
        "cpu": "5m",
        "memory": "5mi",
    }
    # 怒砍舊副本數
    deployment = apps_v1.read_namespaced_deployment(name=close, namespace=namespace)
    deployment.spec.replicas = 1
    apps_v1.replace_namespaced_deployment(name=close, namespace=namespace, body=deployment)

    # 怒砍舊副本資源
    pods = v1.list_namespaced_pod(namespace=namespace, label_selector=f"app={close}")
    for pod in pods.items:
        pod_name = pod.metadata.name
        pod.spec.containers[0].resources.requests = old_resource_requests
        v1.replace_namespaced_pod(name=pod_name, namespace=namespace, body=pod)
    return jsonify({'g': "g"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=31314)