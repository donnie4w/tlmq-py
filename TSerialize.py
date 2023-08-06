"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
import json
import time

from thrift.protocol.TCompactProtocol import TCompactProtocol
from thrift.transport.TTransport import TMemoryBuffer
from ttypes import *
import zlib
import binascii


def TEncode(ts):
    tmb = TMemoryBuffer()
    ts.write(TCompactProtocol(tmb))
    return tmb.getvalue()


def TDecode(bs, ts):
    tmb = TMemoryBuffer(value=bs)
    ts.read(TCompactProtocol(tmb))
    return ts


def JEncode(data):
    return json.dumps(data).encode('utf-8')


def JDecode(loadstr):
    return json.loads(loadstr)


def intCrc32(value) ->int:
    return  crc32(long2byte(value))
#param int
def crc32(bs) -> int:
    return binascii.crc32(bs)

def long2byte(value) -> bytes:
    return value.to_bytes(8, 'big')

def byte2long(value):
    return int.from_bytes(value, 'big')

def zlibUncz(bs)->bytes:
    do=zlib.decompressobj()
    return do.decompress(bs)

if __name__ == "__main__":
    bp = MqBean()
    bp.id = 111111
    bp.topic = "wuxiaodong"
    bp.msg = "jobjob".encode('utf-8')
    bs = TEncode(bp)
    print(bs)

    bp2 = TDecode(bs, MqBean())
    print(bp2.id)
    print(bp2.topic)
    print(bp2.msg)

    data = {"id": 111, "topic": "nono", 'msg': 'bp.msg'}

    loadstr = JEncode(data)
    print(loadstr)

    data2 = JDecode(loadstr)
    print(data2)

    print(intCrc32(int(time.time_ns())))
    value = 12345678910
    b = long2byte(value)
    print(len(b)," == ", b)
    print(byte2long(b))