FROM python:3.8

COPY requirements.txt  .

Run pip install --upgrade pip

RUN pip install -r requirements.txt

COPY   ./app  ./app

COPY ./serving_dir ./serving_dir  

WORKDIR ./app

CMD [ "uvicorn","main:app" ,"--reload" ,"--host","0.0.0.0","--port","8000" ]

