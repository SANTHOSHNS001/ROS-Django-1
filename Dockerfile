FROM PYTHON:3.11

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /code

RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations && \
    python manage.py migrate

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]