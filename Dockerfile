FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y python mysql-server python-mysqldb nginx uwsgi vim curl telnet && apt clean

EXPOSE 80

COPY src/ /var/www/fi.sgreg/
COPY etc/nginx/sites-enabled/sgreg.fi /etc/nginx/sites-enabled/
COPY etc/uwsgi/apps-enabled/sgreg.fi.ini /etc/uwsgi/apps-enabled/

COPY db/ /db
RUN chmod +x /db/createdb.sh && /db/createdb.sh

COPY --chmod=755 entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]

CMD ["tail", "-f", "/var/log/nginx/access.log", "/var/log/nginx/error.log"]

