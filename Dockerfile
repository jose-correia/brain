FROM python:3.6

RUN mkdir jeec
ADD . /jeec/jeec_brain
WORKDIR /jeec/jeec_brain/

RUN pip install -r ./requirements.txt
