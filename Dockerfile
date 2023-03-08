FROM python:3.8.13-slim

WORKDIR /app
COPY requirements.txt  /app/

# default to use the CPU 
#ENV CUDA_VISIBLE_DEVICES 0

# install pipenv
RUN pip install pipenv
# set up pipenv environment
RUN pipenv run pip install -r requirements.txt
