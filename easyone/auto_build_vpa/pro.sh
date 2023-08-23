#!/bin/sh
s1=$1
s2=$2
s3=$3
# 指定Prometheus的API端點URL
prometheus_url="http://prometheus-kube-prometheus-prometheus.pro.svc.cluster.local:9090/api/v1/query_range"

# 使用curl發送GET請求
response=$(curl -G  --data-urlencode "$s2" --data-urlencode "$3" --data-urlencode "step=10s" "$prometheus_url")

echo $response

# values=$(echo "$response" | jq -r '.data.result[0].values[] | [.[0], .[1]] | @csv')

# # 創建 CSV 檔案
# filename="pro.csv"
# echo "time,value" > "$filename"    # 寫入欄位名
# echo "$values" >> "$filename"      # 寫入提取值
# cp pro.csv /shared-data/pro.csv
