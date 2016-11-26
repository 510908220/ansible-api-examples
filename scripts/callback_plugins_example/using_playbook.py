# -*- encoding: utf-8 -*-
import json
import os
import uuid

import ansible.inventory
import ansible.playbook
from ansible import callbacks, utils

ansible.constants.HOST_KEY_CHECKING = False

hosts = ["192.168.33.101"]
example_inventory = ansible.inventory.Inventory(hosts)

# set job id
os.environ['MY_JOB_ID'] = str(uuid.uuid4())

# setting callbacks
stats = callbacks.AggregateStats()
playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

# creating the playbook instance to run, based on "test.yml" file
pb = ansible.playbook.PlayBook(
    playbook="test.yml",
    stats=stats,
    callbacks=playbook_cb,
    runner_callbacks=runner_cb,
    inventory=example_inventory,
    private_key_file="/root/.ssh/id_rsa",
)

print "yy pid is:", os.getpid()
# running the playbook
pr = pb.run()

# Ensure on_stats callback is called
# for callback modules
playbook_cb.on_stats(pb.stats)

# print the summary of results for each host
print "results:", json.dumps(pr, sort_keys=True, indent=4, separators=(',', ': '))
