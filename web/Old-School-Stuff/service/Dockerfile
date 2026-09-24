FROM php:8.5-apache

# Install mysqli
RUN docker-php-ext-install mysqli

# Install MariaDB
RUN apt-get update && \
    apt-get install -y mariadb-server && \
    rm -rf /var/lib/apt/lists/*

# Disable the Docker image's global "Options -Indexes"
RUN sed -i 's/Options -Indexes/Options FollowSymLinks/' /etc/apache2/conf-enabled/docker-php.conf

# Copy custom Apache config
COPY apache/legacy.conf /etc/apache2/conf-available/legacy.conf

#Enable the conf
RUN a2enconf legacy

# Copy website
COPY NTUPortal/ /var/www/html/

# Copy database
COPY database/init.sql /init.sql

# Copy startup script
COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
