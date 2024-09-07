#!/bin/bash
cd backend
export FLASK_APP=app.py
export FLASK_ENV=production
flask run --host=172.20.70.254 --port=5555
