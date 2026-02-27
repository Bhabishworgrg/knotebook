from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class DevServer(ThreadingHTTPServer):
    def __init__(self, host: str, port: int):
        super().__init__((host, port), SimpleHTTPRequestHandler)
