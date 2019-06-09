import sys, pandas as pd

def parse_parameter(p):
    name, value = p.rstrip().split('=') if p.find('=') != -1 else (p, '')
    words = value.split('+') if value else []
    return name, words

def parse_parameters(params):
    params_dict = {}
    for p in params.split('&'):
        pp = parse_parameter(p)
        params_dict[pp[0]] = pp[1]
    return params_dict

def parse_parameters2(params):
    names = []
    allwords = []
    for p in params.split('&'):
        pp = parse_parameter(p)
        names.append(pp[0])
        allwords = allwords + pp[1]
    return names, allwords
        

def parse_body(b):
    return parse_parameters(b)

def parse_body2(b):
    return parse_parameters2(b)

def parse_url(url, uselesspart = 'http://localhost:8080'):
    path_and_parameters = url[len(uselesspart):]
    path, parameters = path_and_parameters.split('?') if path_and_parameters.find('?') != -1 else (path_and_parameters, [])
    path_parts = path.split('/')
    l_parameters = parse_parameters(parameters) if parameters else []
    return path_parts, l_parameters

def parse_url2(url, uselesspart = 'http://localhost:8080'):
    path_and_parameters = url[len(uselesspart):]
    path, parameters = path_and_parameters.split('?') if path_and_parameters.find('?') != -1 else (path_and_parameters, [])
    path_parts = path.split('/')
    pnames, words = parse_parameters2(parameters) if parameters else ([], [])
    return path_parts, pnames, words

def parse_request(r):
    method, url, version = r.split()
    
    path, parameters = parse_url(url)

    return {'method': method, 'path': path, 'parameters': parameters, 'version': version} 

def parse_request2(r):
    method, url, version = r.split()

    path, par_names, words = parse_url2(url)
    
    return {'method': method, 'path': path, 'par_names': par_names, 'words': words, 'version': version} 

def saveincsv(r, f = sys.argv[1] + '.csv'):
    with open(f, 'w') as csvfile:
        writer = csv.DictWriter(csvfile)
        writer.writeheader()

def possible_values(rs, rpart):
    s = set()
    for r in rs:
        [s.add(l) for l in r[rpart]]
    return s


def all_locations(rs):
    locations = set()
    for r in rs:
        [locations.add(l) for l in r['path']]
    return locations

def all_parameters_names(rs):
    names = set()
    for r in rs:
        names.add(r['parameters'])

def fill_row(tb, r, rpart):
    for k, v in tb.items():
        count = r[rpart].count(k)
        if count > 0:
            v.append(count)
        else:
            v.append(0)

def make_table(rs):
    table = dict()
    locations_tb = dict()
    param_names_tb = dict()
    words_tb = dict()
    table['method'] = []
    table['version'] = []

    locations = possible_values(rs, 'path')
    param_names = possible_values(rs, 'par_names')
    words_in_values = possible_values(rs, 'words')
    
    for l in locations:
        locations_tb[l] = []
    for pn in param_names:
        param_names_tb[pn] = []
    for w in words_in_values:
        words_tb[w] = []
    
    for r in rs:
        table['method'] += r['method']

        fill_row(locations_tb, r, 'path')
        fill_row(param_names_tb, r, 'par_names')
        fill_row(words_tb, r, 'words')

        table.update(locations_tb)
        table.update(param_names_tb)
        table.update(words_tb)
        
        table['version'] += r['version']

        return table
           
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
                    names, words = parse_body2(line)
                    requests[-1]['par_names'] += names
                    requests[-1]['words'] += words
                elif newrequest:
                    requests.append(parse_request2(line)) # If it's the first line of a request, parse it.
                    newrequest = False
   
    print(len(requests))
    df = pd.DataFrame(make_table(requests))
    print(df.head())
    # }}}

main()
