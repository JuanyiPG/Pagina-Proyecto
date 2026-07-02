#!/usr/bin/env bash
set -o errexit

pip install -r requirement.text

pyrhon manage.py collectstatic --no-input
python manage.py 