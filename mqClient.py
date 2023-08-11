"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
from abc import ABC, abstractmethod


class MqClient(ABC):
    @abstractmethod
    def pullByteHandler(self, f):
        pass

    @abstractmethod
    def pullJsonHandler(self, f):
        pass

    @abstractmethod
    def pubByteHandler(self, f):
        pass

    @abstractmethod
    def pubJsonHandler(self, f):
        pass

    @abstractmethod
    def pubMemHandler(self, f):
        pass

    @abstractmethod
    def ackHandler(self, f):
        pass

    @abstractmethod
    def errHandler(self, f):
        pass

    @abstractmethod
    def before(self, f):
        pass

    @abstractmethod
    def connect(self, f):
        pass

    @abstractmethod
    def sub(self, topic) -> int:
        pass

    @abstractmethod
    def subCancel(self, topic) -> int:
        pass

    @abstractmethod
    def pubByte(self, topic, msg) -> int:
        pass

    @abstractmethod
    def pubJson(self, topic, msg) -> int:
        pass

    @abstractmethod
    def pubMem(self, topic, msg) -> int:
        pass

    @abstractmethod
    def pullByte(self, topic, id) -> int:
        pass

    @abstractmethod
    def pullJson(self, topic, id) -> int:
        pass

    @abstractmethod
    def pullByteSync(self, topic, id):
        pass

    @abstractmethod
    def pullJsonSync(self, topic, id):
        pass

    @abstractmethod
    def pullIdSync(self, topic):
        pass

    # setup requires a client return receipt
    @abstractmethod
    def recvAckOn(self, sec) -> int:
        pass

    # set the limit of the size of protocol data sent by the server before compression(Unit:MB)
    @abstractmethod
    def mergeOn(self, size) -> int:
        pass

    @abstractmethod
    def setZlib(self, on) -> int:
        pass
