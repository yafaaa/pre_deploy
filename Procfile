web: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && gunicorn project4.wsgi:application --bind 0.0.0.0:$PORT
