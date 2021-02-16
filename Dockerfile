FROM python:3.6

RUN mkdir /jeec_brain
RUN mkdir -p /jeec_brain/static/members
RUN mkdir -p /jeec_brain/static/squads
RUN mkdir -p /jeec_brain/static/rewards
RUN mkdir -p /jeec_brain/static/companies/images
RUN mkdir -p /jeec_brain/static/speakers/companies
RUN mkdir -p /jeec_brain/static/speakers
RUN mkdir -p /jeec_brain/static/events/images

WORKDIR /jeec_brain

ADD requirements.txt /jeec_brain
RUN pip install -r requirements.txt

ADD . /jeec_brain
RUN python manage.py db migrate
RUN python manage.py db upgrade

EXPOSE 8081

RUN chmod ugo+rwx ./deployment/entrypoint.sh
ENTRYPOINT ["sh", "deployment/entrypoint.sh"]
