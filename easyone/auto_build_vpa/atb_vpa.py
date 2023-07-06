from kubernetes import client, config, watch
import time
import threading
import subprocess
from datetime import datetime

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

if __name__ == '__main__':
    main()

# 建立 Kubernetes API 的客戶端
api_client = client.ApiClient()
vpa_info = client.CustomObjectsApi(api_client)

# 設定要查詢的標籤選擇器條件
# 設定 Deployment 的標籤
target_label = "auto_build_vpa=ye"  # 替換成你想要辨識的標籤




# 觸發查詢prometheus的函數
def handle_trigger():
    now_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # 觸發後等待10分鐘後執行        
    time.sleep(60)
    final_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # 手動串詢問的PQL，我爛
    s1="http://prometheus-kube-prometheus-prometheus.pro.svc.cluster.local:9090/api/v1/query_range?query=django_http_requests_total_by_method_total&start="
    s1=s1+str(now_time)+"&end="+str(final_time)+"&step=10s"
    print(s1)
    subprocess.run(['sh', 'pro.sh', s1])



# 自動獲取VPA資料
def vpaget(namespace,deployment_name):
    for i in range(6) :
        time.sleep(10)
        vpa = vpa_info.get_namespaced_custom_object(
        group="autoscaling.k8s.io",
        version="v1",
        namespace=namespace,
        plural="verticalpodautoscalers",
        name=deployment_name+"-vpa",
        )
        recommendations = vpa["status"]["recommendation"]["containerRecommendations"]
        with open("b.txt", 'a') as file:
            file.write(recommendations[0]["target"]["cpu"]+" "+recommendations[0]["target"]["memory"] + '\n')
    print("b.txt")
    subprocess.run(['sh', 'vpaget.sh'])


# 查詢符合標籤的 Deployment
while True:
    deploy_api = client.AppsV1Api(api_client)
    deploy_list = deploy_api.list_deployment_for_all_namespaces(label_selector=target_label)
    vpa_api = client.CustomObjectsApi(api_client)
    vpa_list = vpa_api.list_cluster_custom_object(
        group="autoscaling.k8s.io",
        version="v1",
        plural="verticalpodautoscalers"
    )
    vpa_names=[]

    for vpa in vpa_list["items"]:
        vpa_name = vpa["metadata"]["name"]
        vpa_names.append(vpa_name)

    # 處理符合條件的 Pod
    for deployment in deploy_list.items:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace
        # 若該VPA存在就跳出循環，
        if deployment_name+"-vpa" in vpa_names:
            # print(f"VPA 'vpa-{deployment_name}' already exists. Skipping creation.")
            continue

        vpa_spec = {    
            "apiVersion": "autoscaling.k8s.io/v1",
            "kind": "VerticalPodAutoscaler",
            "metadata":{
                "name": deployment_name+"-vpa",
                "namespace": namespace
            },
            "spec":{
                "targetRef":{
                    "apiVersion": "apps/v1",
                    "kind": "Deployment",
                    "name":  deployment_name,
                    "namespace": namespace
                },
                "updatePolicy":{
                    "updateMode": "Off"
                }
            }
        }
        vpa_api.create_namespaced_custom_object(
                group="autoscaling.k8s.io",
                version="v1",
                namespace=namespace,
                plural="verticalpodautoscalers",
                body=vpa_spec
            )
        vpa = vpa_info.get_namespaced_custom_object(
        group="autoscaling.k8s.io",
        version="v1",
        namespace=namespace,
        plural="verticalpodautoscalers",
        name=deployment_name+"-vpa",
        )
        while not "status" in vpa:
            vpa = vpa_info.get_namespaced_custom_object(
            group="autoscaling.k8s.io",
            version="v1",
            namespace=namespace,
            plural="verticalpodautoscalers",
            name=deployment_name+"-vpa",
            )
            time.sleep(1)
        with open("b.txt", 'a') as file:
            recommendations = vpa["status"]["recommendation"]["containerRecommendations"]
            file.write(recommendations[0]["target"]["cpu"]+" "+recommendations[0]["target"]["memory"] + '\n')
        get_vpa = threading.Thread(target=vpaget, args=(namespace,deployment_name))
        get_pro = threading.Thread(target=handle_trigger)
        get_pro.start()
        get_vpa.start()

    time.sleep(1)





