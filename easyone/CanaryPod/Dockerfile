# 使用k6基礎image
FROM loadimpact/k6

# 將k6腳本添加到image中
COPY k6.js /docker_k6/


# 運行k6腳本
CMD ["run", "/docker_k6/k6.js"]
