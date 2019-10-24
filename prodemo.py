#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time         : 2019/10/23 19:13
# @Author       : Li Hongwei
# @Email        : lihongwei@integritytech.com.cn
# @File         : prodemo.py
# @Software     : PyCharm

import concurrent.futures
import asyncio
import time
from multiprocessing import Process
from threading import Thread
import logging
import logging.handlers


def create_logger(debug=False, file=False):
    formatter = logging.Formatter('[%(name)s] %(asctime)s [%(levelname)s] %(filename)s:%(lineno)s: %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    if file:
        file_handler = logging.handlers.RotatingFileHandler("app.log", maxBytes=1024 * 1024 * 20,
                                                            backupCount=3)
        file_handler.setFormatter(fmt=formatter)
        file_handler.setLevel(logging.INFO)
        logging.root.addHandler(hdlr=file_handler)

    if debug:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(fmt=formatter)
        console_handler.setLevel(logging.DEBUG)
        logging.root.addHandler(hdlr=console_handler)

    logging.root.setLevel(logging.NOTSET)

    return logging.root


logger = create_logger(debug=True)


async def async_io(name, num):
    await asyncio.sleep(num)
    logging.info(f"[async_io][{name}]start")
    logging.info(f"[async_io][{name}]创建一个阻塞任务")
    await process_task(name, 2)


def block_io(name):
    logging.info(f"[bock_io][{name}]start")
    time.sleep(5)
    logging.info(f"[bock_io][{name}]end")


async def process_task(name, woker=1):

    loop = asyncio.get_running_loop()

    if woker != 1:
        with concurrent.futures.ThreadPoolExecutor(woker) as executor:
            workers = [loop.run_in_executor(executor, block_io, name+str(i)) for i in range(woker)]
            await asyncio.gather(*workers)
    else:
        await loop.run_in_executor(None, block_io, name)


class MyApp(object):

    def __init__(self):
        self.loop = None
        self.max_process = None
        self.max_thread = None
        self.run_process = None

    async def worker(self):
        while True:
            # queue.pull()
            asyncio.run_coroutine_threadsafe(async_io("张三", 3), self.loop)
            asyncio.run_coroutine_threadsafe(async_io("李四", 2), self.loop)

    async def create_server(self):
        while True:
            # queue.push()
            pass

    def create_loop(self):
        loop = asyncio.new_event_loop()

        def __start_loop(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        run_loop_thread = Thread(target=__start_loop,
                                 args=(loop,)
                                 )  # 新起线程运行事件循环, 防止阻塞主线程
        run_loop_thread.start()  # 运行线程，即运行协程事件循环

        return loop

    def start_app(self):
        if self.loop is None:
            self.loop = self.create_loop()
        if self.max_process:
            if self.run_process:
                self.max_process -= self.run_process
            executor = concurrent.futures.ProcessPoolExecutor(self.max_process)
            self.loop.set_default_executor(executor)
        elif self.max_thread:
            executor = concurrent.futures.ThreadPoolExecutor(self.max_thread)
            self.loop.set_default_executor(executor)

        asyncio.run(self.worker())

    def run(self, run_process=None):
        if not run_process:
            self.start_app()
        else:
            self.run_process = run_process
            for _ in range(run_process):
                t = Process(target=self.start_app)
                t.start()


if __name__ == '__main__':
    app = MyApp()
    # app.max_thread = 10
    # app.max_process = 10
    app.run()
