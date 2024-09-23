FROM python:3.11
RUN apt-get update -y && apt-get upgrade -y

RUN pip install requests
RUN pip install qdrant-client

WORKDIR /app
COPY main.py /app
RUN chmod +x main.py
CMD ["python", "main.py"]
