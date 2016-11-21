# ansible api自定义插件

## 插件加载目录
插件加载位置是由```DEFAULT_CALLBACK_PLUGIN_PATH```控制的，可以看[constants.py](https://github.com/ansible/ansible/blob/devel/lib/ansible/constants.py). 默认的插件加载位置是:
```
~/.ansible/plugins/callback_plugins:/usr/share/ansible_plugins/callback_plugins
```
为了不影响全局配置,这里是直接修改变量```ansible.constants.DEFAULT_CALLBACK_PLUGIN_PATH```的值来加载我们自己的插件.

## 插件执行的说明
一个简单的插件如图:
```
def log(host, category, data):
    with open(host + category, "w") as f:
        f.write("{0},{1},{2}".format(datetime.datetime.now(), category, data))

class CallbackModule(object):

    def runner_on_failed(self, host, res, ignore_errors=False):
        log(host, 'failed', res)

    def runner_on_ok(self, host, res):
        log(host, 'ok', res)

    def runner_on_skipped(self, host, item=None):
        log(host, 'skipped', item)

    def runner_on_unreachable(self, host, res):
        log(host, 'unreachable', res)

    def playbook_on_stats(self, stats):
        """Complete: Flush log to database"""
        pass
```

注意:插件的回调是针对playbook里每一个任务的, 比如有三个任务, 如果三个任务都执行成功了都会调用runner_on_ok. 所以要记录日志可不能直接```log(host, 'ok', res)```,这样只会显示最后一次的日志记录.

准备在```CallbackModule```里设置一个变量,去保存各个回调的输出. 类似于这样:
```
class CallbackModule(object):
    def __init__(self):
        self.detailed_results = defaultdict(list)

    def playbook_on_start(self):
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.detailed_results[host].append({'failures': res})

    def runner_on_ok(self, host, res):
        self.detailed_results[host].append({'ok': res})
        print "ok!:", self.detailed_results, id(self.detailed_results)

    def runner_on_skipped(self, host, item=None):
        self.detailed_results[host].append({'skipped': item})

    def runner_on_unreachable(self, host, res):
        self.detailed_results[host].append({'unreachable': res})

    def playbook_on_stats(self, stats):
        """Complete: Flush log to database"""
        hosts = stats.processed.keys()

        summary = {}

        for h in hosts:
            t = stats.summarize(h)
            summary[h] = t

        with open(stats.monitor_name, 'w') as f:
            f.write(str(summary))
        with open(stats.monitor_name + "detail", "w") as f:
            f.write(json.dumps(self.detailed_results))
```
但是```self.detailed_results```却一直为空,我在每一个回调里都打印了```self.detailed_results```的内存地址,发现都是一样的. 但是为什么结果还是为空呢? 最后我在回调里打印了一下进程id:
- ```__init__```和```playbook_on_stats```都是在主进程执行的.
- ```其他```回调都是不同的进程id.

那么,还是得老老实实的在每一个回调里保存日志了. 但是我需要区别每一次playbook的执行情况. 怎么办呢? 查询资料最后的方法是使用环境变量:
```
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
```
因为插件机制就是这样的,所以利用环境变量传递变量是个很好的办法. 这样可以详细的记录playbook每次执行信息:
- ```playbook_on_stats```记录执行的一个汇总(成功多少,失败多少等)
- ```其他回调```记录任务每一次执行详情.
