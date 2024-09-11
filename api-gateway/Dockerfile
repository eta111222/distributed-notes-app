FROM nginx:latest

COPY ./nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY ./ssl/server.key /etc/ssl/private/server.key
COPY ./ssl/server.crt /etc/ssl/certs/server.crt

EXPOSE 80
EXPOSE 443

CMD ["nginx", "-g", "daemon off;"]