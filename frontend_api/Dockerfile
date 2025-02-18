FROM python:3.11.1-alpine3.17
ENV PYTHONUNBUFFERED=1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /frontend_api

COPY requirements.txt .
RUN pip3 install -r requirements.txt 

COPY . .

RUN python manage.py collectstatic --noinput

ENV DJANGO_SETTINGS_MODULE=frontend_api.settings

EXPOSE 8000

CMD ["gunicorn", "frontend_api.wsgi:application", "--workers", "3", "--bind", "0.0.0.0:8000"]