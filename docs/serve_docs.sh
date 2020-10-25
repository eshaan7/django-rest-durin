#!/usr/bin/env bash
export DJANGO_SETTINGS_MODULE="example_project.settings"
make html
cd build/html && python3 -m http.server 6969 && cd ../../