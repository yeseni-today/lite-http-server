from lite_http import *

"""
手动测试🌺
"""

request = """GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: keep-alive\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nDNT: 1\r\n\r\n
"""

re = Request(request, ('localhost', 8080))
print(re.method)
print(re.path)
print('----')
print(re.signature)
print('----')
print(re.headers)
