#Load a Docker Imge for python to an InferenceAPI
FROM python:3.9-slim
#create a work directory /code
WORKDIR /inference-demo

COPY requirements.txt requirements.txt

#Install all libraries
RUN pip install -r requirements.txt

COPY . .

WORKDIR /inference-demo/bioscanner
CMD python app.py -p 5000:5000
