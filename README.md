# LULimsuck
這是我目前論文的前配置，但是我爛所以我只有做一點點，希望之後可以補上

首先，畢竟是k8s相關，使用kubeadm建立k8s叢集，安裝期間我一律建議sudo su
在那之前先裝Docker，問就是爽抄學長：
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

等個大概三分鐘不到，init就會建立完畢，接著就是基礎的flannel和污點消除，污點消除後確認一下Node狀態484已經Ready了
```
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl taint nodes --all node-role.kubernetes.io/master-
```

現在是istio時間
```
```
