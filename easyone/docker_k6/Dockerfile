# 使用k6基礎映像
FROM loadimpact/k6

# 將k6腳本添加到映像中
COPY k6.js /docker_k6/


# 運行k6腳本
CMD ["run", "/docker_k6/k6.js"]
