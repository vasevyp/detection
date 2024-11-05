#!/bin/bash
python -Xutf8 manage.py dumpdata --format=json --indent=4 --output=data.json 