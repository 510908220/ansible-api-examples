#!/usr/bin/python
import subprocess
import json
try:
    subprocess.check_output("ps auxc | grep nginx", shell=True)
except:
    print json.dumps({"value": "nginx not exists"})
else:
    print json.dumps({"value": "nginx exist!"})
