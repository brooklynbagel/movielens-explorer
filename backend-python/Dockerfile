FROM python:3.9

RUN pip install --no-cache-dir \
  pipenv==2021.5.29 \
  gunicorn==20.1.0

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

COPY app.py helpers.py query_prep.py test_query_prep.py /app/

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "app:app" ]
