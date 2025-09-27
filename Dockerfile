FROM python:3.11.2-slim-buster

WORKDIR /usr/src/app

# install untuk pdfkit
# RUN apt-get update && apt-get install -y 

COPY ./requirements.txt .
COPY ./.env .
RUN pip install -r requirements.txt

EXPOSE 8010

COPY . .

# CMD [ "poetry", "run", "uvicorn", "main:app","--host", "0.0.0.0", "--port", "8010", "--reload"]
CMD [ "uvicorn", "main:app","--host", "0.0.0.0", "--port", "8010"]
# CMD [ "uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000", "--reload" ,"--log-config", "log_conf.json"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--loop", "uvloop", "--http", "httptools", "--backlog", "2048", "--reload"]