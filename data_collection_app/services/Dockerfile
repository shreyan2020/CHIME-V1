# pull official base image
FROM python:3.8.10-slim-buster

# set work directory
WORKDIR /usr/local/services/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install netcat -y

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/local/services/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/local/services/

EXPOSE 5000

# run entrypoint.sh
#ENTRYPOINT ["/usr/local/services/entrypoint.sh"]

RUN python manage.py flush --no-input
RUN python manage.py makemigrations --no-input
RUN python manage.py migrate --no-input

CMD ["gunicorn", "--workers=2", "admin.wsgi:application", "--bind", "0.0.0.0:5000"]