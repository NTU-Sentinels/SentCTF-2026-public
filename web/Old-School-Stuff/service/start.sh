#!/bin/bash

service mariadb start

sleep 5

mysql -u root < /init.sql

/usr/local/bin/apache2-foreground
