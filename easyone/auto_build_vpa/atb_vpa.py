from kubernetes import client, config
import time


def main():
    config.load_incluster_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" %
              (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


if __name__ == '__main__':
    main()

# 建立 Kubernetes API 的客戶端
api_client = client.ApiClient()

# 設定要查詢的標籤選擇器條件
# 設定 Deployment 的標籤
target_label = "auto_build_vpa=ye"  # 替換成你想要辨識的標籤

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
        # 在這裡可以執行你想要的自動化操作
        # existing_vpa = vpa_api.get_namespaced_custom_object(
        #     group="autoscaling.k8s.io",
        #     version="v1",
        #     namespace=namespace,
        #     plural="verticalpodautoscalers",
        #     name=deployment_name,
        # )

        #若該VPA存在就跳出循環
        if deployment_name+"-vpa" in vpa_names:
            print(f"VPA 'vpa-{deployment_name}' already exists. Skipping creation.")
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
        print(f"Created VPA for deploy: {deployment_name}")

    time.sleep(5)