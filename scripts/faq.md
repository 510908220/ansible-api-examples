
## 远程主机公钥指纹提示
```
The authenticity of host '192.168.56.101 (192.168.56.101)' can't be established.
ECDSA key fingerprint is 32:c8:65:36:26:82:cf:6a:8c:83:5d:d0:89:33:9e:69.
Are you sure you want to continue connecting (yes/no)?
```
如何避免呢? 实际这个可以由```HOST_KEY_CHECKING```变量控制的. 点击这里查看[constants.py](https://github.com/ansible/ansible/blob/devel/lib/ansible/constants.py)
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
