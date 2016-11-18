# encoding:utf-8
import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import json

# the fastest way to set up the inventory

# hosts list
hosts = ["192.168.56.101"]
# set up the inventory, if no group is defined then 'all' group is used by default
example_inventory = ansible.inventory.Inventory(hosts)
ansible.constants.HOST_KEY_CHECKING = False # 会自动在know_hosts添加的
pm = ansible.runner.Runner(
    module_name='command',
    module_args='uname -a',
    timeout=5,
    inventory=example_inventory,
    subset='all',  # name of the hosts group
    private_key_file="/root/.ssh/id_rsa",
    remote_user='root',
    # remote_pass = 'user password'
)

out = pm.run()

print json.dumps(out, sort_keys=True, indent=4, separators=(',', ': '))
