#FROM python:3.11.8
#LABEL authors="sribalaji"
#WORKDIR /code
#
#COPY . /code/wddapi
#
#RUN pip install --no-cache-dir --upgrade -r /code/wddapi/requirements.txt
#
#CMD ["python","main.py"]
FROM alpine:3.19

RUN apk update && apk upgrade

# I used 3.11.8
RUN apk add --no-cache python3=3.11.9-r0
RUN apk add --no-cache py3-pip
RUN apk add --no-cache build-base

RUN echo "contact@isribalaji.in" > /etc/apk/default-entrypoint

WORKDIR /code

COPY . /code/wddapi

RUN pip3 install --no-cache-dir --upgrade --break-system-packages -r /code/wddapi/requirements.txt

EXPOSE 8080

#CMD ["python", "main.py"]
CMD ["uvicorn", "device:app", "--host", "0.0.0.0", "--port", "8080", "--reload", "--log-level", "debug"]