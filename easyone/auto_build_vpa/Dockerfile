# 使用 Python 3.9 為基礎image
FROM python:3.9

# 設定工作目錄
WORKDIR /auto_build_vpa

# 將程式碼複製到容器內
COPY ./atb_vpa.py .
COPY ./vpaget.sh .
COPY ./pro.sh .
COPY ./sent_pro.sh .

# 安裝 Flask 套件
RUN apt-get update
RUN apt-get install -y jq
RUN pip3 install kubernetes

# 開放指定的通訊埠
# EXPOSE 8080

# 執行 Python 程式碼
CMD ["chmod", "u+x", "*.sh"]



