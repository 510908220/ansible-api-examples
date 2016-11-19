# 基于Ansible的监控

## 监控概述

- 远程主机特定进程是否存活
- 采集主机信息并展示,如磁盘、cpu等
- 监控数据库，如mysql、rabitmq等


## 告警
- 支持邮件
- 微信
- 平台事件

## 技术方案

## 错误记录

##### 问题1

```
- hosts: all
  gather_facts: no
  tasks:
  - name: Copy file
    copy: src=/vagrant_data/pamc_monitor/util/check_nginx_process.py dest=/opt/test.py owner=root mode=755
  - name: Execute script
    command: /opt/test.py
```
错误
```
failed: [192.168.33.101] => {"cmd": "/opt/test.py", "failed": true, "rc": 2}
msg: [Errno 2] No such file or directory
failed: [192.168.33.102] => {"cmd": "/opt/test.py", "failed": true, "rc": 2}
msg: [Errno 2] No such file or directory

FATAL: all hosts have already failed -- aborting
```
原因


#### 问题2
```
ansible aliyun -i inve.cfg -m script -a 'check_nginx.sh'  -vvvv
```

```
82.92.67.22 | FAILED >> {
    "changed": true,
    "rc": 127,
    "stderr": "OpenSSH_5.9p1 Debian-5ubuntu1.10, OpenSSL 1.0.1 14 Mar 2012\ndebug1: Reading configuration data /etc/ssh/ssh_config\r\ndebug1: /etc/ssh/ssh_config line 19: Applying options for *\r\ndebug1: auto-mux: Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_request_forwards: requesting forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 9963\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 127\r\nShared connection to 182.92.67.22 closed.\r\n",
    "stdout": "/bin/sh: 1: /root/.ansible/tmp/ansible-tmp-1479548001.19-82988123484984/check_nginx.sh: not found\r\n"
}

```

```
 Trying existing master\r\ndebug2: fd 3 setting O_NONBLOCK\r\ndebug2: mux_client_hello_exchange: master version 4\r\ndebug3: mux_client_request_forwards: requesting forwardings: 0 local, 0 remote\r\ndebug3: mux_client_request_session: entering\r\ndebug3: mux_client_request_alive: entering\r\ndebug3: mux_client_request_alive: done pid = 9963\r\ndebug3: mux_client_request_session: session request sent\r\ndebug1: mux_client_request_session: master session id: 2\r\ndebug3: mux_client_read_packet: read header failed: Broken pipe\r\ndebug2: Received exit status from master 127\r\nShared connection to 182.92.67.22 closed.\r\n",
```

 Trying existing master\r\ndebug1: mux_client_request_session: master session id: 2\r\nShared connection to 172.16.61.2 closed.\r\n
