ARG TENSORFLOW_VERSION=1.14.0-gpu-py3
FROM tensorflow/tensorflow:${TENSORFLOW_VERSION}

WORKDIR /

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends curl

RUN mkdir /app

COPY model/*.tar /app/
WORKDIR /app
RUN tar xvf *.tar
RUN rm *.tar

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY main.py /app/main.py
COPY index.html /app/index.html

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
