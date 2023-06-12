# LULimsuck
目前已經做好使用django的django-prometheus配件強行被prometheus監控了（你各位本機測試安裝套件的時候先確認python3 run的是不是root用戶，還有root用戶一般用戶有沒有pip3 install）


本次新增的部份是：1.部屬prometheus，並且新增參數(balue.yaml)監控使用django的pu。2.使用pu作為接收網路流量請求的接收方以此提高http請求數量或者CPU使用率，並且藉此讓KEDA使用指標來縮放。


目前還缺乏讓KEDA縮放的能力，以及後續或許可以用PredictKube來接續七天後的prometheus的監控，穩定度更高。


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


部署自動建立vpa和自動獲取vpa資訊，條件是label有"auto_build_vpa=ye"，你各位image我設定的是本地搜尋啊，記得建立本地的
```
kubectl apply -f vpa_in_one.yaml
```


cloneyaml服務負責將進來的檔案「999.yaml」轉為實際檔名並且加上v2，send_to_host服務接收POST請求後轉送POST請求給storgev2，applyv2是失敗的（媽的k8s_client到現在還是不回我問題）
```
cd cloneyaml
kubectl apply -f cloneyaml.yaml
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
