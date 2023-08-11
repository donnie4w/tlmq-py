"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
import _thread
from simpleclient import *
import time

if __name__ == "__main__":
    sc = SimpleClient("ws://127.0.0.1:5100", "mymq=123")
    sc.pullByteHandler(lambda mb: logging.debug("PullByteHandler >> " + str(mb)))
    sc.pullJsonHandler(lambda mb: logging.debug("PullJsonHandler >> " + str(mb)))
    sc.pubByteHandler(lambda mb: logging.debug("PubByteHandler >> " + str(mb)))
    sc.pubJsonHandler(lambda mb:  logging.debug("PubJsonHandler >> " + str(mb)))
    sc.pubMemHandler(lambda mb:  logging.debug("PubMemHandler >> " + str(mb)))
    sc.ackHandler(lambda aid: logging.debug("ack id>> " + str(aid)))
    sc.errHandler(lambda code: logging.error("err code >>" + str(code)))
    sc.before(lambda : logging.debug("before >>"))
    logging.debug("python mqcli demo run")
    # cd.connect 阻塞当前线程
    _thread.start_new_thread(sc.connect, ())
    time.sleep(1)
    # sc.recvAckOn(60)  # 客户端ack确认收到信息，否则服务器不认为信息已送达，将一直发送, 60s 设定服务器重发时间
    sc.mergeOn(10)  # 10M 设定服务器发送协议数据压缩前大小上限
    # sc.setZlib(True)
    sc.sub('usertable')  # 订阅 topic “usertable”
    # sc.subCancel('usertable')  # 取消订阅 topic “usertable”
    sc.sub('usertable2')  # 订阅 topic “usertable2”
    sc.sub('usertable3')  # 订阅 topic “usertable2”

    ack = sc.pubByte('usertable', bytearray('this is python pubByte', 'utf-8'))  # 发布topic usertable及信息
    logging.debug(ack)
    ack = sc.pubJson('usertable', 'this is python pubByte')
    logging.debug(ack)
    sc.pubMem('usertable', 'this is python pubMem')
    id = sc.pullJson("usertable", 10)
    logging.debug("id=" + str(id))

    id = sc.pullIdSync('usertable')
    logging.debug("PullIdSync >>" + str(id))

    mb = sc.pullByteSync('usertable', 1)
    logging.debug("mb >>" + str(mb))

    jmb = sc.pullJsonSync('usertable', 1)
    logging.debug("mb >>" + str(jmb))

    time.sleep(1000)
