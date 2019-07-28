#!/bin/bash

#
# Copyright (c) 2019 Petuum, Inc. All rights reserved.
#
set -ex
echo "Launching package-manager."

python manage.py makemigrations pkgMgr
python manage.py migrate
sleep 1
python manage.py runserver 0.0.0.0:8000
