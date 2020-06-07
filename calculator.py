"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

"""
import traceback

def home():
    page = """
        <h1>WSGI Calculator</h1>
        <p>A simple calculator to perform the following functions with two numbers: <b>add</b>, <b>subtract</b>, <b>multiply</b>, <b>divide</b></p>
        <p><b><i>To Use</i></b>:  Append the function selected to the URL followed by the first and second operand</p>
        <p><i>Example</i>:  http://localhost:8080/<u>divide</u>/<u>22</u>/<u>11</u></p>
    """
    return page

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    return str(sum(map(int, args)))

def subtract(*args):
    """ Returns a STRING with the difference of the arguments """

    return str(int(args[0])-int(args[1]))

def multiply(*args):
    """ Returns a STRING with the product of the arguments """

    return str(int(args[0])*int(args[1]))

def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    quotient, remainder = divmod(*map(int, args))
    return str(quotient)

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '': home,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
    }
    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        # body = func(*args)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Can't Divide By Zero</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
