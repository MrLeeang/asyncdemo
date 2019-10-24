#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time         : 2019/10/23 15:34
# @Author       : Li Hongwei
# @Email        : lihongwei@integritytech.com.cn
# @File         : testasync+pro.py
# @Software     : PyCharm

import concurrent.futures
import asyncio
import time


def bock_io(name):
    time.sleep(10)
    print(f"[bock_io][{name}]我终于跑完了")


async def async_io(name):
    await asyncio.sleep(5)
    print(f"[async_io][{name}]我终于跑完了")


async def task(num):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(5) as executor:
        t1 = loop.run_in_executor(executor, bock_io, "小明"+str(num))
        t2 = loop.run_in_executor(executor, bock_io, "小红"+str(num))

        await t1, t2

    # t3 = asyncio.create_task(async_io("小伟"))
    # await t3
    # await async_io("小李"), t1, t2


async def main():
    await asyncio.gather(task(1), task(2))


if __name__ == '__main__':
    start = time.clock()
    asyncio.run(main())
    elapsed = (time.clock() - start)
    print("Time used: {}".format(elapsed))
