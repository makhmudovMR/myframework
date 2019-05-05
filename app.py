from wsgiref.simple_server import make_server
from api import API

app = API()

@app.route('/home')
def home(request, response):
    response.text = "hello from home method"


@app.route('/about')
def about(request, response):
    response.text = "hello from about method"

server = make_server('localhost', 8000, app=app)
server.serve_forever()