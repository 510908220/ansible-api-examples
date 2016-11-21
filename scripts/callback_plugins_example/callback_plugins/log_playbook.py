import os


class CallbackModule(object):
    def __init__(self):
        self.job_id = os.environ['MY_JOB_ID']

    def playbook_on_start(self):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        print host, self.job_id

    def runner_on_ok(self, host, res):
        print host, self.job_id

    def runner_on_skipped(self, host, item=None):
        pass

    def runner_on_unreachable(self, host, res):
        print host, self.job_id

    def playbook_on_stats(self, stats):
        """Complete: Flush log to database"""
        hosts = stats.processed.keys()
        summary = {}

        for h in hosts:
            t = stats.summarize(h)
            summary[h] = t
        print self.job_id, summary
