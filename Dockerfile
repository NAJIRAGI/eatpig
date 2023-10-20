FROM python:3.9.0

WORKDIR /home/

RUN echo "test4"

RUN git clone https://github.com/NAJIRAGI/eatpig.git

WORKDIR /home/eatpig/

RUN pip install -r requirements.txt

RUN pip install gunicorn

RUN pip install mysqlclient

EXPOSE 8000

CMD ["bash", "-c", "python manage.py collectstatic --noinput --settings=eatpig.settings.deploy && python manage.py migrate --settings=eatpig.settings.deploy && gunicorn eatpig.wsgi --env DJANGO_SETTINGS_MODULE=eatpig.settings.deploy --bind 0.0.0.0:8000"]