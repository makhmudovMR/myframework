from webob import Request, Response

class API:

    def __init__(self):
        '''
            routes
            path: handler_function
        '''
        self.routes = {}


    def __call__(self, environ, start_response):
        '''магический метод выполняет функцию приложения'''
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)


    # следует изучить принцип работы данной конструкции
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper


    def handle_request(self, request):
        '''функция обработчик принимает запрос и выдаёт ответ'''
        response = Response()

        handler = self.find_handler(request.path)

        if handler is not None:
            handler(request, response)
        else:
            self.default_response(response)
        return response


    def find_handler(self, request_path):
        ''' ищет обработчик по заданному пути'''
        for path, handler in self.routes.items():
            if path == request_path:
                return handler
        return None


    def default_response(self, response):
        ''' функция обработчик для несуществующих страниц'''
        response.status_code = 404
        response.text = "Not found."