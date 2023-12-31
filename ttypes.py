#
# Autogenerated by Thrift Compiler (0.17.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class MqBean(object):
    """
    Attributes:
     - topic
     - id
     - msg

    """


    def __init__(self, topic=None, id=None, msg=None,):
        self.topic = topic
        self.id = id
        self.msg = msg

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.topic = iprot.readString().decode('utf-8', errors='replace') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.id = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.msg = iprot.readBinary()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('MqBean')
        if self.topic is not None:
            oprot.writeFieldBegin('topic', TType.STRING, 1)
            oprot.writeString(self.topic.encode('utf-8') if sys.version_info[0] == 2 else self.topic)
            oprot.writeFieldEnd()
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I64, 2)
            oprot.writeI64(self.id)
            oprot.writeFieldEnd()
        if self.msg is not None:
            oprot.writeFieldBegin('msg', TType.STRING, 3)
            oprot.writeBinary(self.msg)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.topic is None:
            raise TProtocolException(message='Required field topic is unset!')
        if self.id is None:
            raise TProtocolException(message='Required field id is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class MergeBean(object):
    """
    Attributes:
     - beanList

    """


    def __init__(self, beanList=None,):
        self.beanList = beanList

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.LIST:
                    self.beanList = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readBinary()
                        self.beanList.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('MergeBean')
        if self.beanList is not None:
            oprot.writeFieldBegin('beanList', TType.LIST, 1)
            oprot.writeListBegin(TType.STRING, len(self.beanList))
            for iter6 in self.beanList:
                oprot.writeBinary(iter6)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.beanList is None:
            raise TProtocolException(message='Required field beanList is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(MqBean)
MqBean.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'topic', 'UTF8', None, ),  # 1
    (2, TType.I64, 'id', None, None, ),  # 2
    (3, TType.STRING, 'msg', 'BINARY', None, ),  # 3
)
all_structs.append(MergeBean)
MergeBean.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'beanList', (TType.STRING, 'BINARY', False), None, ),  # 1
)
fix_spec(all_structs)
del all_structs
