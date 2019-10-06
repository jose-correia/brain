FROM python:3.7.4

RUN mkdir jeec
ADD . /jeec/jeec_brain
WORKDIR /jeec/jeec_brain/

RUN pip install --no-cache-dir -r ./requirements.txt