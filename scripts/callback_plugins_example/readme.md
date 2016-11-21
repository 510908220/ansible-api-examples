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

那还是老老实实在每一句会调里都打印一条日志, 但是要是插入数据库的话如果一个playbook有很多task,很多host的话数据库插入是很频繁的. 所以还是想着怎么能汇总起来进行一次插入就好了. 所谓山重水复疑无路,柳暗花明又一村. 在python里有一个类```Manager```可以实现多个进程操作同一个列表或字典. 看官方的例子:
```
from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    manager = Manager()

    d = manager.dict()
    l = manager.list(range(10))

    p = Process(target=f, args=(d, l))
    p.start()
    p.join()

    print d
    print l
```
输出:
```
{0.25: None, 1: '1', '2': 2}
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```
希望来了, 上代码:

```

import json
from multiprocessing import Process, Manager
from collections import defaultdict


class CallbackModule(object):
    def __init__(self):
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
```
现在已经可以将一次playbook执行的信息汇总起来了. 但是还缺少怎么去标识这一次任务执行呢?
在网上苦寻一番,解决方案是利用环境变量.
- 在playbook里设置:  ```os.environ['MY_JOB_ID'] = str(uuid.uuid4())```
- 在插件里读取:
```
class CallbackModule(object):
    def __init__(self):
        self.job_id = os.environ['MY_JOB_ID']
        self.result_list = Manager().list()

    def playbook_on_start(self):
        pass
```

## 参考
- [how-to-pass-data-to-my-callback](http://grokbase.com/t/gg/ansible-devel/14c2qm038n/how-to-pass-data-to-my-callback)
