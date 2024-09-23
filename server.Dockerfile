FROM python:3.9 AS model_downloader
RUN apt-get update -y && apt-get upgrade -y 
RUN apt install -y p7zip-full
RUN pip install gdown
RUN gdown 1Y9TMjj04fVhNuJnhzaM4Wmn2CQfZ8r8U
RUN 7z x /DeepStyle.7z
RUN mkdir /model
RUN mv /DeepStyle/model/94bef_ep32/epochs/epoch0032/tf_model.h5 /model
RUN mv /DeepStyle/model/94bef_ep32/epochs/epoch0032/config.json /model
RUN mv /DeepStyle/model/94bef_ep32/epochs/epoch0032/scores.json /model

FROM python:3.7 AS server
COPY --from=model_downloader /model /model
RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install -y libhdf5-dev

RUN git clone https://github.com/hayj/DeepStyle /vendor/DeepStyle
RUN pip install -e /vendor/DeepStyle

WORKDIR /app
EXPOSE 80

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
COPY server.py server.py
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
