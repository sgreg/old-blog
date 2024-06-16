#!/bin/bash

/etc/init.d/mysql start
/etc/init.d/uwsgi start
/etc/init.d/nginx start

echo "Up and running!"

exec "$@"

