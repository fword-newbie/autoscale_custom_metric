# 使用 Python 3.9 為基礎映像
FROM python:3.9

# 設定工作目錄
WORKDIR /auto_build_vpa

# 將程式碼複製到容器內
COPY ./atb_vpa.py .

# 安裝 Flask 套件
RUN pip3 install kubernetes

# 開放指定的通訊埠
# EXPOSE 8080

# 執行 Python 程式碼
#  CMD ["python3","atb_vpa.py"]



