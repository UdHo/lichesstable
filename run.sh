#!/bin/bash

python main.py && git add -A && git commit -m "Data update $(date)" && git push
