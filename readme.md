### mq client for tldb in python

------------

See the example at  http://tlnet.top/tlmq

```go
实例化
sc = SimpleClient("wss://127.0.0.1:5000", "mymq=123")
连接服务器
sc.connect()
该函数阻塞，可以启动新的线程；如：
 _thread.start_new_thread(sc.connect, ())
设置处理函数
sc.pullByteHandler(lambda mb: logging.debug("PullByteHandler >> " + str(mb)))
sc.pullJsonHandler(lambda mb: logging.debug("PullJsonHandler >> " + str(mb)))
sc.pubByteHandler(lambda mb: logging.debug("PubByteHandler >> " + str(mb)))
sc.pubJsonHandler(lambda mb:  logging.debug("PubJsonHandler >> " + str(mb)))
sc.pubMemHandler(lambda mb:  logging.debug("PubMemHandler >> " + str(mb)))
sc.ackHandler(lambda aid: logging.debug("ack id>> " + str(aid)))
sc.errHandler(lambda code: logging.error("err code >>" + str(code)))
sc.before(lambda : logging.debug("before >>"))
```