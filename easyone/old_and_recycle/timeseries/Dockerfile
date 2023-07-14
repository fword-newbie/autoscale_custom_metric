# 使用 Python 3.9 為基礎image
FROM python:3.9

# 設定工作目錄
WORKDIR /timeseries


# 將程式碼複製到容器內
COPY ./timeseries.py .

# 安裝 Flask 套件
RUN pip3 install darts

# 開放指定的通訊埠
# EXPOSE 8080

# 執行 Python 程式碼
# CMD ["chmod", "u+x", "*.sh"]



