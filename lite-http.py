import socket, threading

log = print


class Request():
    def __init__(self, orign_request):
        self.orignal_request = orign_request
        self.signature = 'undefined'
        twopart = [x for x in orign_request.split('\r\n\r\n') if x]
        self.headers = dict()
        self.parse_headers_and_signature(twopart[0])
        if len(twopart) == 2:
            # request have body
            self.body = twopart[1]

    def parse_headers_and_signature(self, headers_part):
        lines = headers_part.split("\r\n")
        self.signature = lines[0]
        # headers of request
        for header in range(1, len(lines)):
            if lines[header].startswith('Host'):
                self.headers['Host'] = lines[header].split(":")[1:]
                continue
            item = lines[header].split(":", 2)
            self.headers[item[0]] = item[1].strip()


class Response():
    pass


template = b"""<!DOCTYPE HTML>
    <html>
    <head>  
        <meta charset="utf-8"/>
        <title> Python Web server</title>
    </head>
    <body>
        <h1>Hello World</h1>
    </body></html>"""


def handle_request(request):
    respone = b'HTTP-Version: HTTP/1.0 200 ok\r\nContent-Type: text/html; charset=UTF-8\r\n' + \
              b'Content-Length: ' + bytes(str(len(template)), encoding='utf-8') + b'\r\n\r\n' + template
    log(respone)
    return respone


def accept_socket(sock: socket, addr):
    while True:
        ori_request = sock.recv(1024)
        if not ori_request:
            break
        request = Request(ori_request.decode('utf-8'))
        log("Accept new http request: %s" % request.signature)
        log("Send http response: %s" % request.signature)
        sock.send(handle_request(request))
    sock.close()


def bad_request():
    pass


def start(host, port):
    global _main
    _main = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _main.bind((host, port))
    _main.listen()
    while True:
        sock, addr = _main.accept()
        log('Accept new connection %s:%s' % addr)
        threading.Thread(target=accept_socket, args=(sock, addr)).start()


def headers(header: dict):
    pass


def not_found():
    pass


start("localhost", 8079)
# start("localhost", 8080)
