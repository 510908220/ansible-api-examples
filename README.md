# ansible-api-examples
整理ansible api的使用.  目前使用ansible版本是1.9.6.

## ansible api例子
- [基本使用](https://github.com/510908220/ansible-api-examples/tree/master/scripts/basi_%20example)
- [在远程主机执行脚本](https://github.com/510908220/ansible-api-examples/tree/master/scripts/execute_local_script_on_remote_server)
- [使用插件去记录任务详细信息](https://github.com/510908220/ansible-api-examples/tree/master/scripts/callback_plugins_example)


## 更进一步

 根据那个插件的例子可以去实现一个监控系统了. 基本信息都满足了:

- 标识任务的id
- 记录ansible playbook每个任务执行的详细信息并存到任务id对应的数据表中

## 运行说明

都是使用私钥去登录远程主机的, 测试的时候换成自己环境的私钥，以及目标ip即可.
