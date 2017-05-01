# -*- coding: utf-8 -*
"""
输出给定文件的信息。
例如输出单个文件的信息: `python examples/fileinfo.py examples/fileinfo.py`
```
========== /user_path/python/examples/fileinfo.py ==========
       size : 3.83KB(0 dirs, 0 files)
create time : 2017-04-30 13:31:05
modify time : 2017-04-30 13:31:05
access time : 2017-04-30 13:31:09
====================================================================
```
输出目录下的信息：`python examples/fileinfo.py examples`
输出多个文件或目录信息：`python examples/fileinfo.py file1 file2`
"""

import sys
import os
import stat
import time


# 文件信息表格，收集文件信息并美化输出结果。
class file_info_table(object):
    def __init__(self, title):
        self.title = title
        self.info = []  # [(key, value), ...]
        self.max_key_len = 0  # 最长的key的长度

    def append(self, key, value):
        self.info.append((key, value))
        if len(key) > self.max_key_len:
            self.max_key_len = len(key)

    def __str__(self):
        res = []

        # 输出文件名
        res.append("%s %s %s" % ('=' * 10, self.title, '=' * 10))
        # 追加键值对，键的长度按最大长度算
        tpl = '\t%' + str(self.max_key_len) + 's : %s'
        for (k, v) in self.info:
            res.append(tpl % (k, v))
        # 输出底边框
        res.append('=' * (20 + 2 + len(self.title)))
        return '\n'.join(res)


# 从sys.argv中获取文件名
def get_filenames_from_args():
    if len(sys.argv) < 2:  # [a.py, arg1, arg2]，至少2个元素才能获得文件名
        return []
    return sys.argv[1:]


# 将size转换成友好的字符串格式,结果保留两位小数,size_b的单位为B。
def size_for_human(size_b):
    min_size_label = [(1 << 40, 'TB'), (1 << 30, 'GB'), (1 << 20, 'MB'),
                      (1 << 10, 'KB')]
    for (min_size, label) in min_size_label:
        if size_b / min_size > 0:
            return '%.2f%s' % (1.0 * size_b / min_size, label)
    return '%.2fB' % (1.0 * size_b)


# 时间戳转换成字符串格式
def timestamp_to_str(ts):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))


# 是否是目录
def isdir(filepath=None, file_stat=None):
    if (not filepath) and (not file_stat):
        return False
    if not file_stat:
        file_stat = os.stat(filepath)
    return stat.S_ISDIR(file_stat[stat.ST_MODE])


# 文件大小，如果是目录则递归查找。
def file_size(file_name, file_stat=None):
    if not file_stat:
        file_stat = os.stat(file_name)
    if not isdir(file_stat=file_stat):
        return file_stat[stat.ST_SIZE]
    # 递归统计该目录下所有文件大小
    sum_size = file_stat[stat.ST_SIZE]
    for child in os.listdir(file_name):
        abs_path = os.path.join(file_name, child)
        sum_size += file_size(abs_path)
    return sum_size


# 返回parent下子目录和子文件的个数。
def num_subdir_subfile(parent):
    if not isdir(filepath=parent):
        return (0, 0)
    num_subdir, num_subfile = 0, 0
    for child in os.listdir(parent):
        abs_path = os.path.join(parent, child)
        if isdir(filepath=abs_path):
            num_subdir += 1
            n1, n2 = num_subdir_subfile(abs_path)
            num_subdir += n1
            num_subfile += n2
        else:
            num_subfile += 1
    return (num_subdir, num_subfile)


# 输出 file_name 指定文件的相关信息
def print_file_info(file_name):
    abs_path = os.path.abspath(file_name)
    file_stat = os.stat(abs_path)
    table = file_info_table(abs_path)

    # 文件大小
    size = file_size(abs_path, file_stat)
    num_dir, num_file = num_subdir_subfile(abs_path)
    table.append('size', '%s(%d dirs, %d files)' % (size_for_human(size),
                                                    num_dir, num_file))
    # 创建时间
    table.append('create time', timestamp_to_str(file_stat[stat.ST_CTIME]))
    # 修改时间
    table.append('modify time', timestamp_to_str(file_stat[stat.ST_MTIME]))
    # 访问时间
    table.append('access time', timestamp_to_str(file_stat[stat.ST_ATIME]))

    print table


def main():
    file_names = get_filenames_from_args()
    for file_name in file_names:
        print_file_info(file_name)


if __name__ == "__main__":
    main()