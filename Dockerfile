FROM python:3.6

RUN mkdir jeec

RUN mkdir -p /jeec/jeec_brain

RUN mkdir -p /jeec/jeec_brain/static/members
RUN mkdir -p /jeec/jeec_brain/static/companies/images
RUN mkdir -p /jeec/jeec_brain/static/speakers/companies
RUN mkdir -p /jeec/jeec_brain/static/speakers
RUN mkdir -p /jeec/jeec_brain/static/events/images

WORKDIR /jeec/jeec_brain

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
