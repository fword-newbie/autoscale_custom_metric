# 使用 Python 3.9 為基礎image
FROM python:3.7

# 設定工作目錄
WORKDIR /CanaryPod

# 將程式碼複製到容器內
COPY ./canary.py .
COPY ./cana.py .
COPY ./pro.sh .
COPY ./c.py .

# 安裝 Flask 套件
RUN apt-get update
RUN apt-get install vim -y
RUN pip3 install Flask
RUN pip3 install requests
RUN pip3 install Kubernetes


# 開放指定的通訊埠
# EXPOSE 8080

# 執行 Python 程式碼
CMD ["chmod", "u+x", "pro.sh"]