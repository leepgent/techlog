#!/bin/bash
GUNICORN=/usr/local/bin/gunicorn
SOCKET=unix:/var/www/techlog/gunicorn.sock
PROJECT_ROOT=$(dirname $0)
PROJECT=techlog.wsgi

cd $PROJECT_ROOT
sudo -u www-data /usr/bin/env - $GUNICORN -b $SOCKET -w 1 $PROJECT
