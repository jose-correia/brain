FROM nginx:alpine

COPY ./nginx/nginx.conf /etc/nginx/
COPY ./nginx/brain.conf /etc/nginx/conf.d/brain.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY ./nginx/ssl/cert.pem /etc/nginx/ssl/cert.pem
COPY ./nginx/ssl/key.pem /etc/nginx/ssl/key.pem

CMD ["nginx"]
