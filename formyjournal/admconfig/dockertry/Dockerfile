FROM python:3.9-slim-buster
WORKDIR /dockertry
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY helloworld.py .
CMD ["python", "helloworld.py"]
