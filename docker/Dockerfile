#Load a Docker Imge for python to an InferenceAPI
FROM python:3.9-slim
#create a work directory /code
WORKDIR /bioscanner

COPY . .

#COPY into file requirements.txt and load from the current folder the requeriments.txt
COPY requirements.txt requirements.txt

#Install all libraries
RUN pip install -r requirements.txt
#Copy from this folder all to the folder /code in docker container
#entry point to run python3 scripts
#CMD gunicorn --bind 0.0.0.0:5000 app:app
CMD python /bioscanner/bioscanner/app.py -p 5000:5000
