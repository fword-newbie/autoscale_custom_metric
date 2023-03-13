FROM ubuntu:20.04
WORKDIR /reqdocker
COPY req.sh /home/script.sh
RUN apt update && apt install -y curl && chmod u+x /home/script.sh
CMD ["sh", "/home/script.sh"]

