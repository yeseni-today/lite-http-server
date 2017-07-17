import socket, threading

log = print

STATIC_DIR = 'static'
REQUEST_MAX_LENGTH = 1024 * 1024

HEADER_CONTENT_TYPE = ('Content-Type', 'text/html; charset=UTF-8')
RESPONSE_FIRST_VERSION = 'HTTP-Version: HTTP/1.0'


class Request():
    def __init__(self, orign_request, addr):
        self.path = None
        self.method = None
        self.signature = None
        self.headers = dict()
        self.body = None
        self.orignal_request = orign_request

        self.host, self.port = addr
        self.__parse_request__(orign_request)

    def __parse_request__(self, request):
        twopart = [x for x in request.split('\r\n\r\n') if x]
        self.__parse_headers_and_signature__(twopart[0])
        if len(twopart) == 2:
            # request have body
            self.body = twopart[1]

    def __parse_headers_and_signature__(self, headers_part):
        lines = headers_part.split("\r\n")
        self.signature = lines[0]
        # headers of request
        for header in range(1, len(lines)):
            if lines[header].startswith('Host'):
                self.headers['Host'] = lines[header].split(":")[1:]
                continue
            item = lines[header].split(":", 2)
            self.headers[item[0]] = item[1].strip()
        self.__parse_method_and_path__()

    def __parse_method_and_path__(self):
        """
        parse like 'GET / HTTP/1.1'
        """
        self.method, self.path, *other = self.signature.split(' ')


class Response():
    __slots__ = ['status', 'headers', 'body', 'message']

    def __init__(self):
        self.headers = dict()

    @classmethod
    def ok(cls, body):
        res = Response()
        res.status = 200
        res.message = 'ok'
        res.body = body
        if body:
            res.headers['Content-Length'] = str(len(body))
        # res.headers
        return res

    def source_view(self):
        """
        将Response转换为Source模式, Type is Bytes
        :return:
        """
        source = str()
        signature = ' '.join([RESPONSE_FIRST_VERSION, str(self.status), self.message])
        headers_str = str()

        for title, content in self.headers.items():
            headers_str += ': '.join([title, content])
            headers_str += '\r\n'
        body = self.body
        source += '\r\n'.join([signature, headers_str])
        if body:
            source += '\r\n\r\n'
            source += body
        return bytes(source, encoding='utf-8')


def handle_request(request: Request):
    """
    handle request and return Response
    """
    if request.method.lower() == 'get':
        return Response.ok(body="""<!DOCTYPE HTML>
                        <html>
                            <head>
                                <meta charset="utf-8"/>
                                <title>Python Web server</title>
                            </head>
                        <body>
                            <h1>Hello World</h1>
                        </body>
                        </html>""")


def accept_socket(sock: socket, addr):
    ori_request = sock.recv(REQUEST_MAX_LENGTH)
    request = Request(ori_request.decode('utf-8'), addr)
    log("Accept new http request: %s" % request.signature)
    log("Send http response: %s" % request.signature)
    response_byte = handle_request(request).source_view()
    log(response_byte)
    sock.send(response_byte)
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


start("0.0.0.0", 8079)
# start("0.0.0.0", 8080)
