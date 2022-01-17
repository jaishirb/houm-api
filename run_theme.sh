docker-compose exec backend python3 manage.py loaddata themes/bt.json \
&& docker-compose exec backend python3 manage.py loaddata themes/dj.json \
&& docker-compose exec backend python3 manage.py loaddata themes/fd.json \
&& docker-compose exec backend python3 manage.py loaddata themes/start.json \
&& docker-compose exec backend python3 manage.py loaddata themes/uws.json