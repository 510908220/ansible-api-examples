# Ansible api之远程执行脚本

## 执行```using_runner.py```
```
root@vagrant-ubuntu-precise-64:/vagrant_data/ansible-api-examples/scripts/execute_local_script_on_remote_server# python using_runner.py
{
    "contacted": {
        "192.168.33.101": {
            "changed": true,
            "invocation": {
                "module_args": "check_nginx_process.py",
                "module_complex_args": {},
                "module_name": "script"
            },
            "rc": 0,
            "stderr": "OpenSSH_5.9p1 Debian-5ubuntu1.10, OpenSSL 1.0.1 14 Mar 2012\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 19: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug1: mux_client_request_session: master session id: 2\r\nShared connection to 192.168.33.101 closed.\r\n",
            "stdout": "{\"value\": \"nginx exist!\"}\r\n"
        }
    },
    "dark": {}
}
```
其中```stdout```为远程脚本的输出,可以根据实际需要输出为json方便解析.

## 执行```using_playbook.py```
> ```check_nginx_process.yml```使用了script模块;```check_nginx_process_1.yml```使用了copy和shell模块. 实现的效果是一样的.


```
root@vagrant-ubuntu-precise-64:/vagrant_data/ansible-api-examples/scripts/execute_local_script_on_remote_server# python using_playbook.py

PLAY [all] ********************************************************************

TASK: [check nginx] ***********************************************************
changed: [192.168.33.101]

TASK: [display check result] **************************************************
ok: [192.168.33.101] => {
    "var": {
        "out": {
            "changed": true,
            "invocation": {
                "module_args": "check_nginx_process.py",
                "module_complex_args": {},
                "module_name": "script"
            },
            "rc": 0,
            "stderr": "OpenSSH_5.9p1 Debian-5ubuntu1.10, OpenSSL 1.0.1 14 Mar 2012\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 19: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug1: mux_client_request_session: master session id: 2\r\nShared connection to 192.168.33.101 closed.\r\n",
            "stdout": "{\"value\": \"nginx exist!\"}\r\n",
            "stdout_lines": [
                "{\"value\": \"nginx exist!\"}"
            ]
        }
    }
}
results: {
    "192.168.33.101": {
        "changed": 1,
        "failures": 0,
        "ok": 2,
        "skipped": 0,
        "unreachable": 0
    }
}
```
playbook的执行结果为```results```,这个一般就是个统计结果. 要看到信息信息可以使用```debug```模块打印出来，远程执行脚本的输出就是```out```下面的```stdout```.
## FAQ
记录一个遇到的坑: 我是使用pycharm创建的```check_nginx_process.py```脚本. 然后执行```using_runner.py```时却出现了下面的错误:
```
root@vagrant-ubuntu-precise-64:/vagrant_data/ansible-api-examples/scripts/execute_local_script_on_remote_server# python using_runner.py
{
    "contacted": {
        "192.168.33.101": {
            "changed": true,
            "invocation": {
                "module_args": "check_nginx_process.py",
                "module_complex_args": {},
                "module_name": "script"
            },
            "rc": 127,
            "stderr": "OpenSSH_5.9p1 Debian-5ubuntu1.10, OpenSSL 1.0.1 14 Mar 2012\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 19: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug1: mux_client_request_session: master session id: 2\r\nShared connection to 192.168.33.101 closed.\r\n",
            "stdout": "/bin/sh: 1: /root/.ansible/tmp/ansible-tmp-1479639007.18-158238881060130/check_nginx_process.py: not found\r\n"
        }
    },
    "dark": {}
}
```
这里提示的是```check_nginx_process.py: not found```，在google搜了许久, 有跟我类似的问题但是并没有答案. 大半天都没找到个结果. 最后我是在远程机器上手动执行了一下脚本,出现如下提示:
```
-bash: ./check_nginx_process.py: /usr/bin/python^M: bad interpreter: No such file or directory
```
网上搜了一下原来是windows下编辑有不可见字符:```脚本文件是DOS格式的, 即每一行的行尾以 来标识, 其ASCII码分别是0x0D, 0x0A.```
解决方法：
-  ```vim filename```
- ```:set ff``` #可以看到dos或unix的字样. 如果的确是dos格式的。
- ```:set ff=unix``` #把它强制为unix格式的, 然后存盘退出。

再次运行脚本。
