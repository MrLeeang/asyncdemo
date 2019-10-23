#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time         : 2019/10/23 19:13
# @Author       : Li Hongwei
# @Email        : lihongwei@integritytech.com.cn
# @File         : prodemo.py
# @Software     : PyCharm
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
from multiprocessing import Process


async def async_io(name):
    await asyncio.sleep(1)
    print(f"[async_io][{name}]我终于跑完了")


def main(name):
    time.sleep(5)
    print(f"[bock_io][{name}]我终于跑完了")


async def run(woker=1):
    # loop = asyncio.get_running_loop()
    # if woker != 1:
    #     with concurrent.futures.ProcessPoolExecutor(woker) as executor:
    #         workers = [loop.run_in_executor(executor, main, "小明") for _ in range(woker)]
    #         await asyncio.gather(*workers)
    # else:
    #     await loop.run_in_executor(None, main, "小明")
    await async_io(woker)


def start(woker=1):
    # asyncio.run(run(woker))
    loop = asyncio.new_event_loop()
    asyncio.run_coroutine_threadsafe(run(woker), loop)
    return loop.run_forever()


if __name__ == '__main__':
    # asyncio.run(run(5))
    # with concurrent.futures.ProcessPoolExecutor(5) as executor:
    #     executor.submit(start("t1"))
    #     executor.submit(start("t2"))
    #     executor.submit(start("t3"))
    #     executor.submit(start("t4"))
    for i in range(5):
        t = Process(target=start, args=(i,))
        t.deamon = True
        t.start()
    start("hahaha")
