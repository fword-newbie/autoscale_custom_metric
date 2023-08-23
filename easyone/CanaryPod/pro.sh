#!/bin/sh
s1=$1
s2=$2
s3=$3

# 使用curl發送GET請求
prometheus_url="http://prometheus-kube-prometheus-prometheus.pro.svc.cluster.local:9090/api/v1/query"
#response=$(curl -G --data-urlencode "$s1"  --data-urlencode "$s2" --data-urlencode "$3" --data-urlencode "step=10s" "$prometheus_url")
response=$(curl -G --data-urlencode "$s1" "$prometheus_url")


echo $response


#curl -G --data-urlencode "query=avg(rate(django_http_requests_total_by_method_total{method=\"POST\"}[30s]))" "http://prometheus-kube-prometheus-prometheus.pro.svc.cluster.local:9090/api/v1/query"
