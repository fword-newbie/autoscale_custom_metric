from kubernetes import client, config, watch
import threading
import json
import time



def main():
    config.load_incluster_config()
    print("Listing pods with their IPs:")
    

if __name__ == '__main__':
    main()


# 建立 VPA 的 API 客戶端
vpa_api = client.CoreV1Api()
vpa_info = client.CustomObjectsApi(client.ApiClient())

# 定義 VPA 物件的 namespace 和 name
vpa_namespace = "default"
vpa_name = "puyuan-v1-vpa"


# 定義觸發時執行的特定程式碼
def execute_specific_code(event):
    for i in range(6) :
        vpa = vpa_info.get_namespaced_custom_object(
        group="autoscaling.k8s.io",
        version="v1",
        namespace=vpa_namespace,
        plural="verticalpodautoscalers",
        name=vpa_name,
        )
        recommendations = vpa["status"]["recommendation"]["containerRecommendations"]
        with open("b.txt", 'a') as file:
            file.write(recommendations[0]["target"]["cpu"]+"  "+recommendations[0]["target"]["memory"] + '\n')
        time.sleep(10)
    
    print("VPA created event triggered")


# 定義監視vpa的函數
def watch_vpa():
    w = watch.Watch()
    for event in w.stream(vpa_api.list_event_for_all_namespaces, watch=True):
        event_type = event['type']
        if event_type == 'ADDED':
            # 檢查事件是否是VPA建立事件
            event_object = event['object']
            if event_object.involved_object.kind == 'VerticalPodAutoscaler':
                thread = threading.Thread(target=execute_specific_code, args=(event,))
                thread.start()
    w.stop()


# 啟動監視Pod的執行緒
watch_thread = threading.Thread(target=watch_vpa)
watch_thread.start()


# 主執行緒繼續執行其他任務
print("Main thread continues executing")


# 等待監視執行緒結束
watch_thread.join()
