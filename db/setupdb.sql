CREATE DATABASE sgreg;
CREATE USER 'sgreg'@'localhost' IDENTIFIED WITH mysql_native_password BY 'sgreg';
GRANT ALL PRIVILEGES ON sgreg.* TO 'sgreg'@'localhost' WITH GRANT OPTION;
