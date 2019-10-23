#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time         : 2019/10/23 10:01
# @Author       : Li Hongwei
# @Email        : lihongwei@integritytech.com.cn
# @File         : run.py.py
# @Software     : PyCharm

import concurrent.futures
import asyncio
import time


async def take_potatos(num):
    for i in range(num):
        await asyncio.sleep(5)
        yield i


async def test(i):
    print(i)
    await asyncio.sleep(5)


async def task(i=1):
    print("Hello world!")
    task = asyncio.create_task(test(i))
    await task
    await asyncio.sleep(5)
    print("Hello again!")
    # async for i in take_potatos(3):
    #     print(i)
    await asyncio.sleep(5)
    print("Hello end!")


def task1():
    print("[task1]start")
    time.sleep(5)
    print("[task1]agin")
    time.sleep(5)
    print("[task1]end")
    return "task1"


def task2():
    print("[task2]start")
    time.sleep(5)
    print("[task2]agin")
    time.sleep(5)
    print("[task2]end")
    return "task2"


async def main():
    # 异步非阻塞代码
    tasks = [task(i) for i in range(3)]
    await asyncio.gather(*tasks)

    # 阻塞代码
    # loop = asyncio.get_running_loop()
    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     start_time = time.time()
    #     t1 = loop.run_in_executor(executor, task1)
    #     t2 = loop.run_in_executor(executor, task2)
    #     print(await t1)
    #     print(await t2)
    #     print("ProcessPoolExecutor time is: {}".format(time.time() - start_time))


if __name__ == "__main__":
    asyncio.run(main())
