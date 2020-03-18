#! /usr/bin/env sh

if [[ ${DEBUG} == 'TRUE' ]] || [[ ${DEBUG} == 'True' ]] || [[ ${DEBUG} == '1' ]]; then
    echo >&2 "Starting debug server..."
    npm i
    npm run serve
else
    echo >&2 "Starting prod server..."
    npm i
    npm run build
    npx serve -s dist -l tcp://0.0.0.0:8080
fi
