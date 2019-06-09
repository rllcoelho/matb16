import sys

def sub_file_paths(file_path):
    pass

def parse_parameter(p):
    name, value = p.rstrip().split('=') if p.find('=') != -1 else (p, None)
    words = value.split('+') if value else None
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
    path, parameters = path_and_parameters.split('?') if path_and_parameters.find('?') != -1 else (path_and_parameters, None)
    path_parts = path.split('/')
    l_parameters = parse_parameters(parameters) if parameters else None
    params_names = set()
    return params_names

def main():
    emptylines, count = (0, 0)
    newrequest = True
    params_names = set()
    
    with open(sys.argv[1]) as datafile:# {{{
        for line in datafile:
            if line == '\n': # If empty line
                emptylines += 1
                if emptylines == 2: # requests have 2 empty lines between each other
                    newrequest = True
                    emptylines = 0;
            else:
                if emptylines == 1: # If a line isn't empty but the last one was, it is the request body
                    request_body = line
                    print(parse_body(request_body))
                elif newrequest:
                    request_type, request_url, request_version = line.split() # If it's the first line of a request, parse it.
                    count += 1
                    params_names = params_names.union(parse_url(request_url))
                    #print("%s %s %s" % (request_type, request_url, request_version))
                    newrequest = False

        #print(count)
    # }}}

main()
