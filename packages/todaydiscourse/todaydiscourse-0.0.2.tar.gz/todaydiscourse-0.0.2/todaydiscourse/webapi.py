import web
from todaydiscourse import core

urls = (
    '/', 'index'
)

def start_web():
    """启动应用程序。"""
    app = web.application(urls, globals())
    app.run()

class index:
    def GET(self):
        """GET请求。"""
        web.header('Content-Type', 'text/html;charset=UTF-8')
        return core.get_discourse()