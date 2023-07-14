#!/bin/bash

# 使用 kubectl get 命令查詢自定義資源
result=$(sudo kubectl get vpa $s1 2>&1)
a="have_resource"
b="no_resource"
# 檢查結果中是否包含錯誤訊息
if [[ $result == *"resources found"* ]]; then
  echo $b
else
  echo $a
fi
