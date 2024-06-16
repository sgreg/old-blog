#!/bin/bash

DIR="$(dirname $0)"

/etc/init.d/mysql start

mysql -u root < $DIR/setupdb.sql
mysql -u sgreg sgreg -psgreg < $DIR/sgregfi.dump.sql

/etc/init.d/mysql stop

