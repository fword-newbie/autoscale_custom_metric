# LULimsuck
進度目前已經取得VPA和prometheus資料，後續就是用時間序列分析將資料分析和預測。


補上安裝和部署的懶人用程式碼，首先是helm：
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```


helm 新增Keda和Prometheus：
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
```


用於資料共享的PVC。
```
kubectl apply -f allstorage.yaml
```


helm 使用balue.yaml部署Prometheus(透過additionalScrapeConfigs這個參數去改，具體來說是先部署pu，然後用clusterip的service改這邊的target的IP和port)：
```
helm install -f balue.yaml prometheus prometheus-community/kube-prometheus-stack -n pro --create-namespace #部署
helm uninstall prometheus prometheus-community/kube-prometheus-stack -n pro #解除
```


如果有需要的話，可以用grafana.yaml開nodeport去看網頁版（幹你娘變了，只能看prometheus的，grafana的失效了）：
```
kubectl apply -f grafana.yaml
```


部署keda：
```
helm install keda kedacore/keda --version 2.9 -n keda --create-namespace
kubectl apply -f dummy.yaml #這個問題後續要解決
```


把那個該死的django普圓部署上去才能進行後續的部署：
```
cd try
kubectl apply -f puyuan.yaml
cd ..
```


部署VPA，之前有建過就要先Down
```
cd vertical-pod-autoscaler
./hack/vpa-up.sh
# ./hack/vpa-down.sh
cd ..
```


部署自動建立vpa和自動獲取vpa資訊，條件是label有"auto_build_vpa=ye"，你各位image我設定的是本地搜尋啊，記得建立本地的。
目前已經把getpro和vpaget兩個應用整合到auto_build_vpa，原始程式碼放在old_and_recycle。
使用shared volume方式把取得的指標和VPA推薦CPU等資料整合進本機的/home/local-pv。
```
kubectl apply -f vpa_in_one.yaml
```


cloneyaml服務負責將進來的檔案「999.yaml」轉為實際檔名並且加上v2，send_to_host服務接收POST請求後轉送POST請求給storgev2，applyv2是失敗的（媽的k8s_client到現在還是不回我問題）
這裡我懶得用成兩個container，預設已經有send_to_host，乖乖apply裡面的cloneyaml.py吧。
```
cd cloneyaml
kubectl apply -f cloneyaml.yaml
kubectl exec -it cloneyaml -- /bin/bash
python3 cloneyaml.py
exit
cd ..
```


storgev2就是開一個Flask API介面，接收send_to_host的POST請求並建立該V2 YAML。
```
cd storgev2
python3 storgev2.py
#然後開一個新的command line。
```


最後就是k6的部份（k6永遠最後）：
```
cd docker_k6
kubectl apply -f k6.yaml #要改的話用js的改
cd ..
```


try下有一個c.sh，要用那個apply yaml，具體來說就是./c.sh puyuan.yaml這樣，因為python客戶端不給Pod內部apply yaml。