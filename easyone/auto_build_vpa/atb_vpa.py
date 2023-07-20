from datetime import datetime
from kubernetes import client, config, watch
import csv
import time
import threading
import subprocess
import requests
import json
import ast

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
    print("istime")
    now_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # 觸發後等待10分鐘後執行        
    time.sleep(600)
    final_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    # 組合PromQL查詢語句
    query_post="query=django_http_requests_total_by_method_total{method=\"POST\"}"
    query_cpu="query=node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate{container=\"puyuan\"}"
    query_start="start="+str(now_time)
    query_end="end="+str(final_time)
    
    result1 = subprocess.run(['sh', 'pro.sh',query_post , query_start, query_end], capture_output=True, text=True)
    result2 = subprocess.run(['sh', 'pro.sh',query_cpu , query_start, query_end], capture_output=True, text=True)
    result1 = ast.literal_eval(result1.stdout)
    result2 = ast.literal_eval(result2.stdout)
    print(result2)
    prd=[]
    cc=len(result1['data']['result'][0]['values'])
    post_pro=result1['data']['result'][0]['values']
    cpu_usage=result2['data']['result'][0]['values']
    for i in range(cc):
        prd.append({"time":datetime.fromtimestamp(post_pro[i][0]),"post_value":post_pro[i][1],"cpu_usage":cpu_usage[i][1]}*1000)

    # 寫入資料到 CSV 檔案
    fieldnames = ["time", "post_value", "cpu_usage"] # no get_pro
    with open("pro.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # 寫入欄位名稱
        writer.writerows(prd)  # 寫入資料
    subprocess.run(['sh', 'sent_pro.sh']) #傳送給PVC


# 自動獲取VPA資料
def vpaget(namespace,deployment_name,cam):
    for i in range(60) :
        time.sleep(10)
        vpa = vpa_info.get_namespaced_custom_object(
        group="autoscaling.k8s.io",
        version="v1",
        namespace=namespace,
        plural="verticalpodautoscalers",
        name=deployment_name+"-vpa",
        )
        
        recommendations = vpa["status"]["recommendation"]["containerRecommendations"]
        cam.append({"cpu":recommendations[1]["target"]["cpu"].strip('m')})#"memory":recommendations[1]["target"]["memory"]})
        
    # 指定 CSV 檔案路徑和欄位名稱
    fieldnames = ["cpu"] #"memory"]

    # 寫入資料到 CSV 檔案
    with open("vpa.csv", mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  # 寫入欄位名稱
        writer.writerows(cam)  # 寫入資料
    subprocess.run(['sh', 'vpaget.sh']) #傳送給PVC


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
    

    # 處理符合條件的 Pod
    for deployment in deploy_list.items:
        deployment_name = deployment.metadata.name
        namespace = deployment.metadata.namespace
        pname=deployment_name+"-vpa"
        
        # 構建請求的 URL
        url = f'http://10.20.1.11:800/if_exist'
        
        # 發送 HTTP POST 請求，傳送 JSON 資料
        a=requests.post(url, data=pname)
        data = json.loads(a.text)["exist"].strip('\n')

        # 若該VPA存在就跳出循環，
        if data == "have_resource":
            continue
        else:
            vpa_spec = {    
                "apiVersion": "autoscaling.k8s.io/v1",
                "kind": "VerticalPodAutoscaler",
                "metadata": {
                    "name": deployment_name+"-vpa"
                },
                "spec": {
                    "targetRef": {
                        "apiVersion": "apps/v1",
                        "kind": "Deployment",
                        "name":  deployment_name,
                        "namespace": namespace
                    },
                    "resourcePolicy": {
                        "containerPolicies": [
                            {
                                "containerName": "puyuan",
                                "minAllowed": {
                                    "cpu": "10m",
                                    "memory": "5Mi"
                                },
                                "maxAllowed": {
                                    "cpu": 1,
                                    "memory": "500Mi"
                                },
                                "controlledResources": [
                                    "cpu",
                                    "memory"
                                ]
                            }
                        ]
                    },
                    "updatePolicy": {
                        "updateMode": "Off"
                    }
                }
            }
            # 建立VPA
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
            print("vpa")
            while not "status" in vpa:
                vpa = vpa_info.get_namespaced_custom_object(
                group="autoscaling.k8s.io",
                version="v1",
                namespace=namespace,
                plural="verticalpodautoscalers",
                name=deployment_name+"-vpa",
                )
                time.sleep(1)
                # 寫入資料到 CSV 檔案
            print("now apply k6")
            cam=[{"cpu":vpa["status"]["recommendation"]["containerRecommendations"][1]["target"]["cpu"].strip('m')}]#,"memory":vpa["status"]["recommendation"]["containerRecommendations"][1]["target"]["memory"].strip('k')}]
            get_vpa = threading.Thread(target=vpaget, args=(namespace,deployment_name,cam))
            get_pro = threading.Thread(target=handle_trigger)
            get_pro.start()
            get_vpa.start()
        
    time.sleep(1)

