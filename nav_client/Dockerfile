# FROM python:3.7-slim-stretch
# ENV PYTHONUNBUFFERED 1
# RUN mkdir -p /app
# RUN pip3 install --disable-pip-version-check --no-cache-dir pipenv
# WORKDIR /app
# COPY Pipfile Pipfile.lock /app/

# RUN pipenv install --system --deploy --ignore-pipfile;
# RUN rm -rf /app/Pipfile*
# CMD ["python3", "./main.py"]


FROM python:3.7
RUN pip install fastapi uvicorn
EXPOSE 80
RUN pip install zeep
COPY . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
