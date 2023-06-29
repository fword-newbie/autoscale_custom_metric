# 使用 Python 3.9 為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /cloneyaml

# 將程式碼複製到容器內
COPY ./cloneyaml.py .
COPY ./send_to_host.py .

# 安裝 Flask 套件
RUN pip3 install PyYAML requests Flask

# 開放指定的通訊埠y
EXPOSE 8080 80

# 執行 Python 程式碼

# CMD ["python3","cloneyaml.py"]



