"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
import threading

from TSerialize import *
from httpclient import *
import websocket

MQ_AUTH = 1
MQ_PUBBYTE = 2
MQ_PUBJSON = 3
MQ_SUB = 4
MQ_PULLBYTE = 5
MQ_PULLJSON = 6
MQ_PING = 7
MQ_ERROR = 8
MQ_PUBMEM = 9
MQ_RECVACK = 10
MQ_MERGE = 11
MQ_SUBCANCEL=12
MQ_CURRENTID=13
MQ_ZLIB=14
MQ_ACK = 0


class Config:
    onMessage, onClose, onOpen, onError = None, None, None, None

    def __init__(self, url, origin, auth) -> None:
        self.url, self.origin, self.auth = url + "/mq", origin, auth
        self.isSSL, self.host, self.port = parseUrl(url)
        self.recvAckOn,self.zlib = False,False

    def __init__(self, url, auth) -> None:
        self.url, self.auth, self.origin = url + "/mq", auth, "http://tldb-mq"
        self.isSSL, self.host, self.port = parseUrl(url)
        self.recvAckOn,self.zlib = False,False

class Cli:
    lock = threading.Lock()
    isError = False

    def __init__(self, conf):
        self.conf = conf
        # websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(conf.url,
                                         on_open=conf.onOpen,
                                         on_message=conf.onMessage,
                                         on_error=conf.onError,
                                         on_close=conf.onClose
                                         )

    def connect(self):
        if self.conf.url.startswith("wss"):
            self.ws.run_forever(origin=self.conf.origin, sslopt={"cert_reqs": ssl.CERT_NONE})
        else:
            self.ws.run_forever(origin=self.conf.origin)

    def close(self):
        self.ws.close()

    def auth(self) -> int:
        b = bytearray(self.conf.auth, 'utf-8')
        return self.send(MQ_AUTH, b)

    def ping(self):
        self.send(tl_type=MQ_PING)

    def send(self, tl_type, bs=None) -> int:
        ackid, r = getMsg(tl_type, bs)
        self._send(r)
        return ackid

    def _send(self,bs):
        with self.lock:
            self.ws.send(bs)

    def PubByte(self, topic, msg) -> int:
        bp = MqBean(topic=topic, msg=msg, id=0)
        bs = TEncode(bp)
        return self.send(MQ_PUBBYTE, bs)

    def PubJson(self, topic, msg) -> int:
        d = {"topic": topic, "msg": msg, "id": 0}
        bs = JEncode(d)
        return self.send(MQ_PUBJSON, bs)

    def PullByte(self, topic, id) -> int:
        bp = MqBean(topic=topic, id=id)
        bs = TEncode(bp)
        return self.send(MQ_PULLBYTE, bs)

    def PullJson(self, topic, id) -> int:
        d = {"topic": topic, "id": id}
        bs = JEncode(d)
        return self.send(MQ_PULLJSON, bs)

    def PubMem(self, topic, msg) -> int:
        d = {"topic": topic, "msg": msg, "id": 0}
        bs = JEncode(d)
        return self.send(MQ_PUBMEM, bs)

    def Sub(self, topic) -> int:
        bs = bytearray(topic, 'utf-8')
        return self.send(MQ_SUB, bs)

    def SubJson(self, topic) -> int:
        bs = bytearray(topic, 'utf-8')
        return self.send(MQ_SUB|0x80, bs)

    def SubCancel(self, topic) -> int:
        bs = bytearray(topic, 'utf-8')
        return self.send(MQ_SUBCANCEL, bs)

    def PullByteSync(self, topic, id) -> MqBean:
        bp = MqBean(topic=topic, id=id)
        bs = TEncode(bp)
        # _, r = getMsg(MQ_PULLBYTE, bs)
        r = bytearray(toBytes(MQ_PULLBYTE) + bs)
        msg = httpPost(self.conf.isSSL, r, self.conf.host, self.conf.port, self.conf.auth, self.conf.origin)
        if msg[0] == MQ_PULLBYTE:
            return TDecode(msg[1:], MqBean())
        elif msg[0] == MQ_ERROR:
            return byte2long(msg[1:9])

    def PullJsonSync(self, topic, id) -> str:
        d = {"topic": topic, "id": id}
        bs = JEncode(d)
        # _, r = getMsg(MQ_PULLJSON, bs)
        r = bytearray(toBytes(MQ_PULLJSON) + bs)
        msg = httpPost(self.conf.isSSL, r, self.conf.host, self.conf.port, self.conf.auth, self.conf.origin)
        if msg[0] == MQ_PULLJSON:
            return JDecode(msg[1:].decode('UTF-8'))
        elif msg[0] == MQ_ERROR:
            return byte2long(msg[1:9])

    def PullIdSync(self, topic) -> int:
        bs = bytearray(topic, 'utf-8')
        # _, r = getMsg(MQ_CURRENTID, bs)
        r = bytearray(toBytes(MQ_CURRENTID)+bs)
        msg = httpPost(self.conf.isSSL, r, self.conf.host, self.conf.port, self.conf.auth, self.conf.origin)
        if msg[0] == MQ_CURRENTID:
            return byte2long(msg[1:9])
        elif msg[0] == MQ_ERROR:
            return byte2long(msg[1:9])

    def RecvAckOn(self, sec=60):
        self.send(MQ_RECVACK, toBytes(sec))

    def SetZlib(self,on=False):
        if on:
            self.send(MQ_ZLIB, toBytes(1))
        else:
            self.send(MQ_ZLIB, toBytes(0))

    def MergeOn(self,size=1):
        self.send(MQ_MERGE, toBytes(size))

    def ackMsg(self,bs):
        b_type = toBytes(MQ_ACK)
        r = bytearray(b_type + long2byte(crc32(bs)))
        self._send(r)

def getMsg(tl_type, bs=None):
    b_type = toBytes(tl_type)
    ackId = intCrc32(getAckId())
    if bs is not None:
        r = bytearray(b_type + long2byte(ackId) + bs)
    else:
        r = bytearray(b_type + long2byte(ackId))
    return  ackId,r


def toBytes(value):
    return value.to_bytes(1, 'big')


seqId = 1

def getAckId() -> int:
    global seqId
    seqId += 1
    return crc32(long2byte(seqId) + long2byte(time.time_ns()))


def parseUrl(wsurl):
    ss = wsurl.split('//', 1)
    isSSl = False
    if wsurl.startswith("wss:"):
        isSSl = True
    s = ss[1].split(":", 1)
    return isSSl, s[0], s[1]
