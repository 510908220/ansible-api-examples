#!/usr/bin/python

import json

import ansible.inventory
import ansible.playbook
import ansible.runner
from ansible import callbacks, utils

ansible.constants.HOST_KEY_CHECKING = False
hosts = ["192.168.33.101"]
example_inventory = ansible.inventory.Inventory(hosts)
inventory = ansible.inventory.Inventory(hosts)

pm = ansible.runner.Runner(
    module_name='script',
    module_args='check_nginx_process.py',
    timeout=5,
    inventory=example_inventory,
    subset='all',  # name of the hosts group
    private_key_file="/root/.ssh/id_rsa",
    remote_user='root',
    forks=1
    # remote_pass = 'user password'
)

out = pm.run()

print json.dumps(out, sort_keys=True, indent=4, separators=(',', ': '))
