#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/24 16:13
# @Author  : ZhangZhao
# @Site    : 
# @File    : jingmi.py
# @Software: PyCharm

# -*- coding: UTF-8 -*-

import queue
import threading
import time
import requests
import eleme
import logger
import mongodb_operation as op
from catch_ele import catchEle
mo = op.operation()
ele = eleme.ElemeApp()
ele.change_device()
exitFlag = 0
items = mo.getLatlon()
class myThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        print ("Starting " + self.name)
        geocode(self.name, self.q)
        print ("Exiting " + self.name)

def geocode(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            item = q.get()
            catchEle.data_thread(item)
            queueLock.release()
        else:
            queueLock.release()
        time.sleep(0.1)




threadList = ["Thread-1", "Thread-2", "Thread-3"]
queueLock = threading.Lock()
workQueue = queue.Queue()
threads = []
threadID = 1

# 创建新线程
for tName in range(50):
    thread = myThread(threadID, f'Thread-{tName}', workQueue)
    thread.start()
    threads.append(thread)
    threadID += 1

# 填充队列
queueLock.acquire()
for item in items:
    workQueue.put(item)
queueLock.release()

# 等待队列清空
while not workQueue.empty():
    pass

# 通知线程是时候退出
exitFlag = 1

# 等待所有线程完成
for t in threads:
    t.join()
print ("Exiting Main Thread")