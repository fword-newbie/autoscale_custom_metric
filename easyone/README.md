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


把那個該死的django普圓部署上去才能進行後續的部署：
```
cd try
kubectl apply -f puyuan.yaml
cd ..
```


helm 使用balue.yaml部署Prometheus(透過additionalScrapeConfigs這個參數去改，具體來說是先部署pu，然後用clusterip的service改這邊的target的IP和port)：
```
helm install -f balue.yaml prometheus prometheus-community/kube-prometheus-stack -n pro --create-namespace #部署
helm uninstall prometheus prometheus-community/kube-prometheus-stack -n pro #解除
```


最後就是k6的部份（這邊等到要測試再改）：
```
cd docker_k6
kubectl apply -f k6.yaml #要改的話用js的改
cd ..
```


如果有需要的話，可以用grafana.yaml開nodeport去看網頁版：
```
kubectl apply -f grafana.yaml
```


部署keda：
```
helm install keda kedacore/keda --version 2.9 -n keda --create-namespace
```
