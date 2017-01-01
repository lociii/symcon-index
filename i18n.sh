#!/usr/bin/env bash

./manage.py makemessages -l de --no-location --no-obsolete --ignore=docs/*
sed -i -n "/POT-Creation-Date/!p" symcon/locale/de/LC_MESSAGES/django.po
./manage.py compilemessages
