web: gunicorn heroku.wsgi -b 0.0.0.0:$PORT
worker: celery worker -A heroku -c 2
beat: celery beat -A heroku
