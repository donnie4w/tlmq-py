"""
Copyright 2023 tldb Author. All Rights Reserved.
email: donnie4w@gmail.com
https://github.com/donnie4w/tldb
https://github.com/donnie4w/tlmq-py
"""
import http.client
import ssl


def httpPost(isSSL, data, host, port, auth, origin) -> bytes:
    if isSSL:
        conn = http.client.HTTPSConnection(host, port=port, context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2))
    else:
        conn = http.client.HTTPConnection(host, port=port)
    conn.request('POST', '/mq2', data, headers={"Origin": origin, 'Cookie': "auth=" + auth})
    response = conn.getresponse()
    r = response.read()
    return r
