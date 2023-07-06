from kubernetes import client, config, watch
import time
import threading
import subprocess
from datetime import datetime


# 加載 Kubernetes 配置
def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()
    

if __name__ == '__main__':
    main()


v1 = client.CoreV1Api()

# 定義監視的Namespace
namespace = "default"

# 避免被多次處理
processed_pods = set()


# 定義處理觸發的函數
def handle_trigger(pod):
    pod_name = pod.metadata.name
    if pod.status.phase == "Running" and pod_name not in processed_pods:
        if "auto_build_vpa" in pod.metadata.labels:
            if pod.metadata.labels["auto_build_vpa"] == "ye":
                processed_pods.add(pod_name)
                now_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                # 觸發後等待10分鐘後執行        
                time.sleep(60)
                final_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                # 手動串詢問的PQL，我爛
                s1="http://prometheus-kube-prometheus-prometheus.pro.svc.cluster.local:9090/api/v1/query_range?query=django_http_requests_total_by_method_total&start="
                s1=s1+str(now_time)+"&end="+str(final_time)+"&step=10s"
                print(s1)
                subprocess.run(['sh', 'pro.sh', s1])

# 定義監視Pod的函數
def watch_pods():
    w = watch.Watch()
    for event in w.stream(v1.list_namespaced_pod, namespace=namespace, watch=True):
        pod = event['object']
        if event['type'] == 'ADDED':
            # 在新執行緒中處理觸發的Pod
            thread = threading.Thread(target=handle_trigger, args=(pod,))
            thread.start()

        # 檢查Pod是否被刪除，結束監視
        if event['type'] == 'DELETED':
            break

    # 停止監視
    w.stop()

# 啟動監視Pod的執行緒
watch_thread = threading.Thread(target=watch_pods)
watch_thread.start()

# 主執行緒繼續執行其他任務
print("Main thread continues executing")

# 等待監視執行緒結束
watch_thread.join()
