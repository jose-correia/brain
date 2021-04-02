FROM nginx:alpine

COPY nginx.conf /etc/nginx/
COPY brain.conf /etc/nginx/conf.d/brain.conf

COPY ssl/cert.pem /etc/nginx/ssl/cert.pem
COPY ssl/key.pem /etc/nginx/ssl/key.pem

CMD ["nginx"]