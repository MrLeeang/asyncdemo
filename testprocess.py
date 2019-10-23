#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time         : 2019/10/23 13:21
# @Author       : Li Hongwei
# @Email        : lihongwei@integritytech.com.cn
# @File         : testprocess.py
# @Software     : PyCharm

import concurrent.futures
import time


def test(n):
    print(f"[{n}]start")
    time.sleep(2)
    print(f"[{n}]run")
    time.sleep(2)
    print(f"[{n}]stop")
    return n


def main():
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as executor:
        task_list = [executor.submit(test, n) for n in range(5)]
        process_results = [task.result() for task in task_list]
        print(process_results)


if __name__ == '__main__':
    main()
