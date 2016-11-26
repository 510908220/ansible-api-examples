import json
from collections import defaultdict
from multiprocessing import Manager, Process


class CallbackModule(object):

    def __init__(self):
        self.job_id = os.environ['MY_JOB_ID']
        self.result_list = Manager().list()

    def playbook_on_start(self):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.result_list.append(
            {
                "host": host,
                "res": res,
                "status": "failures"
            }
        )

    def runner_on_ok(self, host, res):
        self.result_list.append(
            {
                "host": host,
                "res": res,
                "status": "ok"
            }
        )

    def runner_on_skipped(self, host, item=None):
        self.result_list.append(
            {
                "host": host,
                "res": '',
                "status": "skipped"
            }
        )

    def runner_on_unreachable(self, host, res):
        self.result_list.append(
            {
                "host": host,
                "res": res,
                "status": "unreachable"
            }
        )

    def playbook_on_stats(self, stats):
        """Complete: Flush log to database"""
        hosts = stats.processed.keys()
        summary = {}

        for h in hosts:
            t = stats.summarize(h)
            summary[h] = t

        task_summary = defaultdict(lambda: defaultdict(list))
        for task_execute_item in self.result_list:
            host = task_execute_item["host"]
            status = task_execute_item["status"]
            res = task_execute_item["res"]
            task_summary[host][status].append(res)

        result = {
            "summary": summary,
            "task_summary": task_summary

        }
        print json.dumps(result, sort_keys=True, indent=4, separators=(',', ': '))
