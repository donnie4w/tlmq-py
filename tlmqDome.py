"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
import _thread
import logging

from simpleClient import *


def PullByteHandler(mb):
    logging.debug("PullByteHandler >> " + str(mb))


def PullJsonHandler(mb):
    logging.debug("PullJsonHandler >> " + str(mb))


def PubByteHandler(mb):
    logging.debug("PubByteHandler >> " + str(mb))


def PubJsonHandler(mb):
    logging.debug("PubJsonHandler >> " + str(mb))


def PubMemHandler(mb):
    logging.debug("PubMemHandler >> " + str(mb))


def AckHandler(aid):
    logging.debug("ack id>> " + str(aid))


def ErrHandler(code):
    logging.error("err code >>" + str(code))


if __name__ == "__main__":
    # sc = SimpleClient("wss://192.168.2.108:5001", "mymq=123")
    sc = SimpleClient("ws://192.168.2.108:5001", "mymq=123")
    sc.PullByteHandler = lambda mb: logging.debug("PullByteHandler >> " + str(mb))
    sc.PullJsonHandler = lambda mb: logging.debug("PullJsonHandler >> " + str(mb))
    sc.PubByteHandler = lambda mb: logging.debug("PubByteHandler >> " + str(mb))
    sc.PubJsonHandler = lambda mb:  logging.debug("PubJsonHandler >> " + str(mb))
    sc.PubMemHandler = lambda mb:  logging.debug("PubMemHandler >> " + str(mb))
    sc.AckHandler = lambda aid: logging.debug("ack id>> " + str(aid))
    sc.ErrHandler = lambda code: logging.error("err code >>" + str(code))
    logging.debug("python mqcli demo run")
    # cd.connect 阻塞当前线程
    _thread.start_new_thread(sc.connect, ())
    time.sleep(1)
    # sc.RecvAckOn(60)  # 客户端ack确认收到信息，否则服务器不认为信息已送达，将一直发送, 60s 设定服务器重发时间
    sc.MergeOn(10)  # 10M 设定服务器发送协议数据压缩前大小上限
    # sc.SetZlib(True)
    sc.Sub('usertable')  # 订阅 topic “usertable”
    # sc.SubCancel('usertable')  # 取消订阅 topic “usertable”
    sc.Sub('usertable2')  # 订阅 topic “usertable2”
    sc.Sub('usertable3')  # 订阅 topic “usertable2”

    ack = sc.PubByte('usertable', bytearray('this is python pubByte', 'utf-8'))  # 发布topic usertable及信息
    logging.debug(ack)
    ack = sc.PubJson('usertable', 'this is python pubByte')
    logging.debug(ack)
    sc.PubMem('usertable', 'this is python pubMem')
    id = sc.PullJson("usertable", 10)
    logging.debug("id=" + str(id))

    id = sc.PullIdSync('usertable')
    logging.debug("PullIdSync >>" + str(id))

    mb = sc.PullByteSync('usertable', 1)
    logging.debug("mb >>" + str(mb))

    jmb = sc.PullJsonSync('usertable', 1)
    logging.debug("mb >>" + str(jmb))
    time.sleep(1000)
