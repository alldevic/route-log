FROM python:3.7-slim-stretch
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /app
RUN pip3 install --disable-pip-version-check --no-cache-dir pipenv
WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy --ignore-pipfile;
RUN rm -rf /app/Pipfile*
CMD ["python3", "./main.py"]
