FROM python:3.6

ARG SECRET_KEY
ENV SECRET_KEY $SECRET_KEY

ARG APP_ENV
ENV APP_ENV $APP_ENV

ARG APP_DB
ENV APP_DB $APP_DB

ARG DATABASE_URL
ENV DATABASE_URL $DATABASE_URL

ARG CLIENT_USERNAME
ENV CLIENT_USERNAME $CLIENT_USERNAME

ARG CLIENT_KEY
ENV CLIENT_KEY $CLIENT_KEY

ARG ROCKET_CHAT_ADMIN_PASSWORD
ENV ROCKET_CHAT_ADMIN_PASSWORD $ROCKET_CHAT_ADMIN_PASSWORD

ARG JWT_SECRET
ENV JWT_SECRET $JWT_SECRET


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

EXPOSE 8081

RUN chmod ugo+rwx ./deployment/entrypoint.sh
ENTRYPOINT ["sh", "deployment/entrypoint.sh"]
