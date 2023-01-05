def output_params_app(environ, start_response):
    res = ['Method: ' + environ['REQUEST_METHOD'] + ';\n']

    res.append('Parameters from header: \n')
    params = environ['QUERY_STRING'].split('&')
    for param in params:
        param = param.replace('=', ': ')
        param += ';\n'
        res.append(param)

    res.append('Body: \n')
    body = environ['wsgi.input'].read(int(environ.get('CONTENT_LENGTH', 0)))
    res.append(body.decode() + '\n')

    res = str.encode("".join(res))

    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return iter([res])


application = output_params_app
