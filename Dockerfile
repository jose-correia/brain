FROM python:3.6

RUN mkdir jeec

RUN mkdir -p /jeec/jeec_brain

WORKDIR /jeec/jeec_brain

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
