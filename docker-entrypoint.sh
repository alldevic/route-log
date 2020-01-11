#! /usr/bin/env sh

set -o errexit
set -o pipefail
cmd="$@"

function postgres_ready() {
    python3 <<END
import sys
import psycopg2
import environ
try:
    env = environ.Env()
    dbname = env.str('POSTGRES_DB')
    user = env.str('POSTGRES_USER')
    password = env.str('POSTGRES_PASSWORD')
    host = env.str('POSTGRES_HOST')
    port = 5432
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
    echo >&2 "Postgres is unavailable - sleeping"
    sleep 1
done

echo >&2 "Postgres is up - continuing..."

echo >&2 "Migrating..."
python3 manage.py migrate

echo >&2 "Collect static..."
python3 manage.py collectstatic --noinput

if [[ ${DEBUG} == 'TRUE' ]] || [[ ${DEBUG} == 'True' ]] || [[ ${DEBUG} == '1' ]]; then
    echo >&2 "Starting debug server..."
    exec python3 manage.py runserver 0.0.0.0:8000
else
    echo >&2 "Starting Gunicorn..."
    exec gunicorn route_log_prj.wsgi:application \
        -k egg:meinheld#gunicorn_worker \
        --name route_log_prj \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        "$@"
fi
