#!/usr/bin/python
import subprocess

try:
    subprocess.check_output("ps auxc | grep nginx", shell=True)
except:
    print {"value": "nginx not exists"}
else:
    print {"value": "nginx exist!"}
