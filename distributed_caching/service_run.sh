#!/usr/bin/env bash
# Service Runner

gunicorn caching:app \
         --certfile=cert.pem \
         --keyfile=key.pem \
         --bind 0.0.0.0:9090 \
         --timeout 2592000 \
         --workers 4 \
         --reload \
         --log-level 'info'
