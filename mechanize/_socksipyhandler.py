from _urllib2_fork import HTTPHandler, HTTPSHandler
import httplib
import socks
import ssl

class SocksiPyConnection(httplib.HTTPConnection):
    def __init__(self, proxytype, proxyaddr, proxyport = None, rdns = True, username = None, password = None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        
class SocksiPyConnectionHttps(httplib.HTTPSConnection):
    def __init__(self, proxytype, proxyaddr, proxyport = None, rdns = True, username = None, password = None, *args, **kwargs):
        self.proxyargs = (proxytype, proxyaddr, proxyport, rdns, username, password)
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        self.sock = ssl.wrap_socket(self.sock, self.key_file, self.cert_file)

class SocksiPyHandler(HTTPHandler, HTTPSHandler):
    handler_order = 50
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksiPyConnection(*self.args, host=host, port=port, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)
        
    def https_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            conn = SocksiPyConnectionHttps(*self.args, host=host, port=port, timeout=timeout, **self.kw)
            return conn
        return self.do_open(build, req)

if __name__ == "__main__":
    #opener = build_opener(SocksiPyHandler(socks.PROXY_TYPE_SOCKS4, 'localhost', 9999))
    print opener.open('http://www.whatismyip.com/automation/n09230945.asp').read()
