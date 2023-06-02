from kubernetes import client, config

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

# 建立 Kubernetes 的 API 客戶端
api_client = client.ApiClient()

# 建立 VPA 的 API 客戶端
vpa_api = client.CustomObjectsApi(api_client)

# 定義 VPA 物件的 namespace 和 name
vpa_namespace = "default"
vpa_name = "puyuan-vpa"

# 使用 API 客戶端查詢 VPA 物件
vpa = vpa_api.get_namespaced_custom_object(
    group="autoscaling.k8s.io",
    version="v1",
    namespace=vpa_namespace,
    plural="verticalpodautoscalers",
    name=vpa_name,
)

# 獲取 VPA 推薦的資源配置
recommendations = vpa["status"]["recommendation"]["containerRecommendations"]
for container in recommendations:
    container_name = container["containerName"]
    cpu = container["target"]["cpu"]
    memory = container["target"]["memory"]
    print(f"Container: {container_name}, CPU: {cpu}, Memory: {memory}")
