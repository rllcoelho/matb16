import sys

def parse_parameter(p):
    name, value = p.rstrip().split('=') if p.find('=') != -1 else (p, None)
    words = value.split('+') if value else []
    return name, words

def parse_parameters(params):
    params_dict = {}
    for p in params.split('&'):
        pp = parse_parameter(p)
        params_dict[pp[0]] = pp[1]
    return params_dict

def parse_body(b):
    return parse_parameters(b)

def parse_url(url, uselesspart = 'http://localhost:8080'):
    path_and_parameters = url[len(uselesspart):]
    path, parameters = path_and_parameters.split('?') if path_and_parameters.find('?') != -1 else (path_and_parameters, [])
    path_parts = path.split('/')
    l_parameters = parse_parameters(parameters) if parameters else []
    return path_parts, l_parameters

def parse_request(r):
    method, url, version = r.split()
    
    path, parameters = parse_url(url)

    return {'method': method, 'path': path, 'parameters': parameters, 'version': version} 

def main():
    emptylines, count = (0, 0)
    newrequest = True
    requests = []

    with open(sys.argv[1]) as datafile:# {{{
        for line in datafile:
            if line == '\n': # If empty line
                emptylines += 1
                if emptylines == 2: # requests have 2 empty lines between each other
                    newrequest = True
                    emptylines = 0;
            else:
                if emptylines == 1: # If a line isn't empty but the last one was, it is the request body
                    requests[-1]['parameters'].append(parse_body(line))
                elif newrequest:
                    requests.append(parse_request(line)) # If it's the first line of a request, parse it.
                    newrequest = False
    for i in range(10):
        print(requests[i])
    # }}}

main()
