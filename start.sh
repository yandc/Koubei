#/bin/sh
#./manage.py runserver 0.0.0.0:5500 &> access.log &
uwsgi uwsgi.ini
