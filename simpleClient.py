"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
import _thread
import logging

from mqcli import *

logging.basicConfig(level=logging.DEBUG, format='%(message)s')


class SimpleClient:
    PullByteHandler = None
    PullJsonHandler = None
    PubByteHandler = None
    PubJsonHandler = None
    PubMemHandler = None
    AckHandler = None
    ErrHandler = None
    subMap = {}
    Before = None

    def __init__(self, url, auth):
        self.MqCli = None
        self.pingCount = 0
        self.conf = Config(url, auth)

    def connect(self):
        self.pingCount = 0
        self.conf.onError = self.onError
        self.conf.onMessage = self.onMessage
        self.conf.onOpen = self.onOpen
        self.conf.onClose = self.onClose
        try:
            self.MqCli = Cli(self.conf)
            self.MqCli.connect()
        except:
            time.sleep(1)
            logging.debug('reconn')
            self.connect()

    # 出错后关闭连接并重新连接
    def onError(self, ws, error):
        logging.error("error")
        time.sleep(1)
        self.MqCli.close()
        self.connect()

    # 处理服务器信息
    def onMessage(self, ws, msg):
        t = msg[0]
        if self.conf.recvAckOn and (
                t == MQ_PULLJSON or t == MQ_PULLBYTE or t == MQ_PUBJSON or t == MQ_PUBBYTE or t == MQ_MERGE):
            self.MqCli.ackMsg(msg)
        self.parse(msg)

    def parse(self, msg):
        t = msg[0]
        if t == MQ_PUBBYTE:
            mb = TDecode(msg[1:], MqBean())
            if self.PubByteHandler is not None:
                self.PubByteHandler(mb)
        elif t == MQ_MERGE:
            if self.conf.zlib:
                print("--------------->1")
                bsz = zlibUncz(msg[1:])
            else:
                bsz = msg[1:]
                print("=================>2")
            if bsz is not None:
                mb = TDecode(bsz, MergeBean())
                if mb is not None:
                    for bl in mb.beanList:
                        self.parse(bl)
        elif t == MQ_PUBJSON:
            mb = JDecode(msg[1:].decode('UTF-8'))
            print(mb)
            if self.PubJsonHandler is not None:
                self.PubJsonHandler(mb)
        elif t == MQ_PUBMEM:
            mb = JDecode(msg[1:].decode('UTF-8'))
            print(mb)
            if self.PubMemHandler is not None:
                self.PubMemHandler(mb)
        elif t == MQ_PULLBYTE:
            mb = TDecode(msg[1:], MqBean())
            if self.PullByteHandler is not None:
                self.PullByteHandler(mb)
        elif t == MQ_PULLJSON:
            mb = JDecode(msg[1:].decode('UTF-8'))
            if self.PullJsonHandler is not None:
                self.PullJsonHandler(mb)
        elif t == MQ_PING:
            self.pingCount -= 1
        elif t == MQ_ACK:
            if self.AckHandler is not None:
                self.AckHandler(byte2long(msg[1:]))
        elif t == MQ_ERROR:
            if self.ErrHandler is not None:
                self.ErrHandler(byte2long(msg[1:]))

    def onClose(self, ws, close_status_code, close_msg):
        pass

    # 连接成功后，新建ping线程
    def onOpen(self, ws):
        self.MqCli.auth()
        time.sleep(1)
        if len(self.subMap) > 0:
            for s in self.subMap.keys():
                self.Sub(s)
        if self.Before is not None:
            self.Before()
        _thread.start_new_thread(self.ping, ())

    def ping(self):
        while True:
            time.sleep(5)
            self.pingCount += 1
            try:
                if self.pingCount > 3:
                    self.MqCli.close()
                    break
                self.MqCli.ping()
            except:
                print("ping error")
                self.MqCli.close()
                break

    def PubByte(self, topic, msg) -> int:
        return self.MqCli.PubByte(topic, msg)

    def PubJson(self, topic, msg) -> int:
        return self.MqCli.PubJson(topic, msg)

    def PullByte(self, topic, id) -> int:
        return self.MqCli.PullByte(topic, id)

    def PullJson(self, topic, id) -> int:
        return self.MqCli.PullJson(topic, id)

    def PubMem(self, topic, msg) -> int:
        return self.MqCli.PubMem(topic, msg)

    def Sub(self, topic) -> int:
        self.subMap[topic] = 0
        return self.MqCli.Sub(topic)

    def SubCancel(self, topic) -> int:
        del self.subMap[topic]
        return self.MqCli.SubCancel(topic)

    def PullByteSync(self, topic, id) -> MqBean:
        return self.MqCli.PullByteSync(topic, id)

    def PullJsonSync(self, topic, id) -> str:
        return self.MqCli.PullJsonSync(topic, id)

    def PullIdSync(self, topic) -> int:
        return self.MqCli.PullIdSync(topic)

    def RecvAckOn(self, sec=60):
        self.conf.recvAckOn=True
        return self.MqCli.RecvAckOn(sec)

    def MergeOn(self, size=1):
        return self.MqCli.MergeOn(size)

    def SetZlib(self, on):
        self.conf.zlib = True
        return self.MqCli.SetZlib(on)
