from wsgiref.simple_server import make_server
from api import API

app = API()

@app.route('/home')
def home(request, response):
    response.text = "hello from home method"


@app.route('/about')
def about(request, response):
    response.text = "hello from about method"


@app.route('/greeting/{name}/')
def greeting(request, response, name):
    response.text = 'Hello {}'.format(name)

if __name__ == '__main__':
    print('Server was start on localhost:8000')
    server = make_server('localhost', 8000, app=app)
    server.serve_forever()
    