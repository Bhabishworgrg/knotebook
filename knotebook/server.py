from urllib.parse import unquote
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from knotebook.constants.content_type import ContentType
from knotebook.renderer import Renderer


class DevHTTPHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.__renderer = Renderer()
        super().__init__(request, client_address, server)


    def do_GET(self) -> None:
        content: str = ''
        content_type: ContentType
        match self.path:
            case '/':
                content = self.__renderer.render_home()
                content_type = ContentType.HTML
            case path if path.endswith('.css'):
                content = self.__renderer.render_exact(self.path.lstrip('/'))
                content_type = ContentType.CSS
            case path if path.endswith('.js'):
                content = self.__renderer.render_exact(self.path.lstrip('/'))
                content_type = ContentType.JS
            case _:
                content = self.__renderer.render_page(unquote(self.path.lstrip('/').rstrip('.md')))
                content_type = ContentType.HTML

        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))


class DevServer(ThreadingHTTPServer):
    def __init__(self, host: str, port: int):
        super().__init__((host, port), DevHTTPHandler)
