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
这是与known_host相关的，另外可以在/etc/ansible/ansible.cfg注释掉:
```
# uncomment this to disable SSH key host checking
# host_key_checking = False

```
不过这个修改是全局的.
