#!/bin/bash
./manage.py dumpdata --natural-foreign -e sessions -e admin -e contenttypes -e auth.Permission --indent=3

