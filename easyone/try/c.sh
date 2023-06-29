#!/bin/bash

# 腳本接受 YAML 檔名作為輸入參數
yaml_file=$1
pod_name="cloneyaml"  # 請將 "your-pod-name" 替換為實際的 Pod 名稱

# 使用 kubectl apply 命令套用 YAML 檔
sudo kubectl apply -f "$yaml_file"

# 將 YAML 檔傳送到指定的 Pod
sudo kubectl cp "$yaml_file" "$pod_name:999.yaml"  # 請將 "/path/to/destination" 替換為實際的目標路徑
