# -*- coding: utf-8 -*
"""
输出系统信息。
使用：`python osinfo.py`
"""

import platform

# platform 的相关函数名称。
profile = [
    'architecture',
    'linux_distribution',
    'mac_ver',
    'machine',
    'node',
    'platform',
    'processor',
    'python_build',
    'python_compiler',
    'python_version',
    'release',
    'system',
    'uname',
    'version',
]

for k in profile:
    if hasattr(platform, k):
        func = getattr(platform, k)
        v = func()
        print '%20s = %s' % (k, v)
