#!/bin/bash
export FLASK_APP=app.py
export FLASK_ENV=production
flask run --host=172.21.2.152 --port=5555
