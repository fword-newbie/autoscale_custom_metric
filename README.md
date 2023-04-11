# LULimsuck
這是我目前論文的前配置，但是我爛所以我只有做一點點，希望之後可以補上

首先，畢竟是k8s相關，使用kubeadm建立k8s叢集，安裝期間我一律建議sudo su，
在k8s之前先裝Docker，問就是爽抄學長：
```
apt update 
apt install -y apt-transport-https \
   ca-certificates \
   curl \
   gnupg-agent \
   software-properties-common   
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"
apt update
apt install -y docker-ce docker-ce-cli containerd.io
service docker start
```

裝完之後換成裝k8s，這不是充版面，而是避免搞混：
```
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt update
apt install -y kubelet=1.23.0-00 kubeadm=1.23.0-00 kubectl=1.23.0-00
```

k8s安裝完畢後再修改Docker的配置，不要問改什麼，自己去翻之前你寫過的鐵人賽描述：
```
cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2"
}
EOF
mkdir -p /etc/systemd/system/docker.service.d
systemctl daemon-reload
systemctl restart docker
```

然後開始部屬，swapoff好像是每過一段時間就會又重新開啟，假如get pod被拒絕又不是因為權限問題的話，嘗試看看swapoff -a
```
swapoff -a
kubeadm init  --pod-network-cidr=10.244.0.0/16
mkdir -p $HOME/.kube
cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
chown $(id -u):$(id -g) $HOME/.kube/config
```

等個大概三分鐘不到，init就會建立完畢，接著就是基礎的flannel和污點消除，可能之後可以試試看用Calico取代flannel進行更高階的操作？污點消除後確認一下Node狀態484已經Ready了
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl taint nodes --all node-role.kubernetes.io/master-
```
接下來，如果有想要將第二台機器加入叢集的話，先重複以上步驟直到kubeadm init不要做，將master-node在建立時所給予的token和sha256在預定的worker-node上面輸入
```
kubeadm join 10.20.1.11:6443 --token ***** \
	--discovery-token-ca-cert-hash sha256:*****
```

然後將worker-node角色命名
```
kubectl label node k8s-worker kubernetes.io/role=worker
```

現在是istio時間，下載、導入路徑、安裝、還有往default的namespace裡面設定自動加sidecar，應該可以透過label的方式固定某些Pod不加
```
curl -L https://istio.io/downloadIstio | sh -
cd istio-1.17.2 #可能因為最新版更改所以要自己注意
export PATH=$PWD/bin:$PATH
istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

但是istio和matrics服務，我最喜歡：
```
kubectl get configmap --all-namespaces
kubectl edit configmap kubelet-config-1.23 --namespace=kube-system
```
```
vim /var/lib/kubelet/config.yaml
```
以上兩個動作都需要更改以加入新內容，更改格式如下：
```
serverTLSBootstrap: true
```
更改後重開kubelet
```
systemctl restart kubelet
```
重啟需要一小段時間，打個手槍什麼的之後再看新證書並准許他
```
kubectl get csr
kubectl certificate approve <來自kubelet-serving的那個>
```
准許後再裝metrics-server
```
cd formyjournal
kubectl apply -f components.yaml
```
今天先到這邊，剩下的等我懶癌發作去世之後再寫
