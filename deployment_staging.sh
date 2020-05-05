#!/bin/bash
cd abang-abang-masif/
git checkout staging
git pull origin staging
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose up -d
docker rm $(docker ps -a -q -f status=exited)
exit