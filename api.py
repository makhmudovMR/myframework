from webob import Request, Response
from parse import parse
from jinja2 import Environment, FileSystemLoader

import inspect
import os


class Api:

    def __init__(self):
        '''
            routes
            path: handler_function
        '''
        self.routes = {} # хранит пути и функции ответы
        self.template_env = Environment(loader=FileSystemLoader(os.path.abspath('templates')))


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
            if inspect.isclass(handler):
                # class based view
                handler_function = getattr(handler(), request.method.lower(), None)
                if handler_function is None:
                    raise AssertionError('Method is not allowed ', request.method)
                handler_function(request, response, **kwargs)
            else:
                # function based view
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

        if path in self.routes:
                raise AssertionError('Such route already exists.')
                
        def wrapper(handler):
            self.routes[path] = handler
            return handler
        return wrapper

    def add_route(self, path, handler):
        if path in self.routes:
            raise AssertionError('Such route already exists')
        
        self.routes[path] = handler

    def default_response(self, response):
        ''' функция обработчик для несуществующих страниц'''
        response.status_code = 404
        response.text = "Not found."

    
    def render(self, template_name, context={}):
        return self.template_env.get_template(template_name).render(**context)