# Ansible Api基本使用

## 运行```runner_example.py```
```
root@vagrant-ubuntu-precise-64:/vagrant_data/ansible-api-examples/scripts/basi_ example# python runner_example.py
{
    "contacted": {
        "192.168.33.101": {
            "changed": false,
            "invocation": {
                "module_args": "",
                "module_complex_args": {},
                "module_name": "ping"
            },
            "ping": "pong"
        }
    },
    "dark": {}
}

```
- ```contacted```: 执行成功
- ```dark```: 执行失败


## 运行```playbook_example.py```
```
root@vagrant-ubuntu-precise-64:/vagrant_data/ansible-api-examples/scripts/basi_ example# python playbook_example.py

PLAY [all] ********************************************************************

TASK: [ping host] *************************************************************
ok: [192.168.33.101]

TASK: [display ping host result] **********************************************
ok: [192.168.33.101] => {
    "var": {
        "out": {
            "changed": false,
            "invocation": {
                "module_args": "",
                "module_complex_args": {},
                "module_name": "ping"
            },
            "ping": "pong"
        }
    }
}
results: {
    "192.168.33.101": {
        "changed": 0,
        "failures": 0,
        "ok": 2,
        "skipped": 0,
        "unreachable": 0
    }
}
```

playbook方式直接看不到详细输出,这里使用了debug模块进行打印.

## FAQ
可以看到脚本里加了这句```ansible.constants.HOST_KEY_CHECKING = False```. 如果不加的话会遇到这样的提示:
```
root@vagrant-ubuntu-precise-64:/vagrant_data/ansible-api-examples/scripts/basi_ example# python runner_example.py
The authenticity of host '192.168.33.101 (192.168.33.101)' can't be established.
ECDSA key fingerprint is 64:b5:be:90:22:92:a0:38:b2:6e:ca:a2:d8:3a:f7:e7.
Are you sure you want to continue connecting (yes/no)?
```
这是与known_host相关的(了解known_hosts可以看阮一峰的[SSH原理与运用（一）：远程登录](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html))， 关于为什么可以这样修改,可以看源码[constants.py](https://github.com/ansible/ansible/blob/devel/lib/ansible/constants.py):
```
def load_config_file():
    ''' Load Config File order(first found is used): ENV, CWD, HOME, /etc/ansible '''
    p = configparser.ConfigParser()
    path0 = os.getenv("ANSIBLE_CONFIG", None)
    if path0 is not None:
        path0 = os.path.expanduser(path0)
        if os.path.isdir(path0):
            path0 += "/ansible.cfg"
    try:
        path1 = os.getcwd() + "/ansible.cfg"
    except OSError:
        path1 = None
    path2 = os.path.expanduser("~/.ansible.cfg")
    path3 = "/etc/ansible/ansible.cfg"

    for path in [path0, path1, path2, path3]:
        if path is not None and os.path.exists(path):
            try:
                p.read(path)
            except configparser.Error as e:
                raise AnsibleOptionsError("Error reading config file: \n{0}".format(e))
            return p, path
    return None, ''
HOST_KEY_CHECKING       = get_config(p, DEFAULTS, 'host_key_checking',  'ANSIBLE_HOST_KEY_CHECKING',    True, value_type='boolean')
```
可以看到```HOST_KEY_CHECKING```是如何取值的. 所以修改可以通过如下方式:
- 修改配置文件```ansible.cfg```, 设置选项```host_key_checking = False```
- 直接修改```HOST_KEY_CHECKING```配置:```ansible.constants.HOST_KEY_CHECKING = False```
实际观察发现这样设置以后回自动在```known_hosts```文件里添加远程主机的公钥.

## 参考
- [Turn off host_key_checking when using Python API](https://groups.google.com/forum/#!topic/ansible-project/5Lg1OsHVMdA)
