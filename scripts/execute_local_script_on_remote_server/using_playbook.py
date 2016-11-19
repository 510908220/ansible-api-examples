# -*- encoding: utf-8 -*-
import json

import ansible.inventory
import ansible.playbook
import ansible.runner
from ansible import callbacks, utils

hosts = ["192.168.33.101"]
example_inventory = ansible.inventory.Inventory(hosts)

# setting callbacks
stats = callbacks.AggregateStats()
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

# creating the playbook instance to run, based on "test.yml" file
pb = ansible.playbook.PlayBook(
    # 也可以使用check_nginx_process_1.yml(使用了copy模块和shell模块)
    playbook="check_nginx_process.yml",
    stats=stats,
    callbacks=playbook_cb,
    runner_callbacks=runner_cb,
    inventory=example_inventory,
    private_key_file="/root/.ssh/id_rsa"
)

# running the playbook
pr = pb.run()

# print the summary of results for each host
print "results:", json.dumps(pr, sort_keys=True, indent=4, separators=(',', ': '))
