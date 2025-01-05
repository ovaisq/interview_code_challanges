#!/usr/bin/env bash
# Service Runner

gunicorn caching:app \
         --bind 0.0.0.0:9090 \
         --timeout 2592000 \
         --workers 2 \
         --reload \
         --log-level 'info'
