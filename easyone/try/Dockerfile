# 使用 Python 3.9 為基礎映像
FROM python:3.7

# 設定工作目錄
WORKDIR /try

# 將程式碼複製到容器內
COPY . .

# 安裝 Django 套件
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install lsof
RUN pip3 install Django==3.2.10
RUN pip3 install prometheus_client
RUN pip3 install django-prometheus
# 開放指定的通訊埠
EXPOSE 80