#!/usr/bin/env bash

pip3 install -r /code/requirements.txt
python3 /code/manage.py migrate

# setup all the configfiles
rm -f /etc/nginx/sites-enabled/default
ln -sf /code/docker/app.conf /etc/nginx/sites-enabled/

# Setting uwsgi settings
mkdir -p /etc/uwsgi/sites/
cp /code/docker/uwsgi.conf /etc/init/uwsgi.conf

# Running wsgi and nginx
service nginx start

# Prepare log files and start outputting logs to stdout
tail -n 0 -f /var/log/nginx/*.log &

uwsgi --ini uwsgi.ini
