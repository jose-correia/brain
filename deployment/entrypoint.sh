#!/bin/bash
exec gunicorn --config /jeec_brain/deployment/gunicorn_config.py manage:app
