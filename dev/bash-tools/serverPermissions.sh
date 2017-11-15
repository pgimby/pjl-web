#! /bin/bash

repositoryDir="/mnt/local/repository"
webDir="/var/www/html"

find $repositoryDir -type d -exec chmod 755 {} \;

