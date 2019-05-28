from wsgiref.simple_server import make_server
from api import Api

app = Api()

@app.route('/home')
def home(request, response):
    response.text = app.render('index.html', {'title': 'Hello world', 'name':'Maga'})


@app.route('/about')
def about(request, response):
    response.text = "hello from about method"


@app.route('/greeting/{name}/')
def greeting(request, response, name):
    response.text = 'Hello {}'.format(name)


@app.route('/books')
class Books:
    def get(self, req, resp):
        resp.text = 'books page'

    def post(self, req, resp):
        resp.text = 'Endpoint to create a book'

        

if __name__ == '__main__':
    print('Server was start on localhost:8000')
    server = make_server('localhost', 8000, app=app)
    server.serve_forever()
    