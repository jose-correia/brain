FROM nginx:alpine

COPY ./nginx/nginx.conf /etc/nginx/
COPY ./nginx/brain.conf /etc/nginx/conf.d/brain.conf
RUN rm /etc/nginx/conf.d/default.conf

CMD ["nginx"]
