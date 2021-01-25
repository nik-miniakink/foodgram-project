FROM nginx:latest
RUN mkdir var/staticfiles
RUN mkdir var/media
RUN rm /etc/nginx/conf.d/default.conf
COPY ./default.conf /etc/nginx/conf.d/default.conf