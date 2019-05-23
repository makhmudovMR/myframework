from webob import Request, Response
from parse import parse


class API:

    def __init__(self):
        '''
            routes
            path: handler_function
        '''
        self.routes = {} # хранит пути и функции ответы


    def __call__(self, environ, start_response):
        '''магический метод выполняет функцию приложения'''
        request = Request(environ)

        response = self.handle_request(request)

        return response(environ, start_response)


    def handle_request(self, request):
        '''функция обработчик принимает запрос и выдаёт ответ'''
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)
        return response

    def find_handler(self, request_path):
        ''' ищет обработчик по заданному пути'''
        for path, handler in self.routes.items():
            parse_result = parse(path, request_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    # следует изучить принцип работы данной конструкции
    def route(self, path):
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper



    def default_response(self, response):
        ''' функция обработчик для несуществующих страниц'''
        response.status_code = 404
        response.text = "Not found."