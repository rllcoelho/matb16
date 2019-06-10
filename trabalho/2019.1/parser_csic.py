import sys, pandas as pd
import pickle, json
from random import sample

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

def save(r, f = sys.argv[1] + '.dict', f_type='pickle'):
    if f_type == 'pickle':
        with open(f + 'pkl', 'wb') as fp:
            pickle.dump(r, fp, protocol=pickle.HIGHEST_PROTOCOL)
    elif f_type == 'json':
        with open(f + 'json', 'w') as fp:
            json.dump(r, fp)


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
    print('Found all possible values for location')
    param_names = possible_values(rs, 'par_names')
    print('Found all possible values for parameter_names')
    words_in_values = possible_values(rs, 'words')
    print('Found all possible values for words in parameter values')
    
    for l in locations:
        locations_tb[l] = []
    for pn in param_names:
        param_names_tb[pn] = []
    for w in words_in_values:
        words_tb[w] = []
    
    c = 0
    lenrs = len(rs)
    for r in rs:
        table['method'].append(r['method'])
        table['version'].append(r['version'])

        fill_row(locations_tb, r, 'path')
        fill_row(param_names_tb, r, 'par_names')
        fill_row(words_tb, r, 'words')
        c += 1

        sys.stdout.write("\r%i/%i" % (c, lenrs))
        sys.stdout.flush()
        #print(len(table))

    table.update(locations_tb)
    print('Locations added to table')
    table.update(param_names_tb)
    print('Par names added to table')
    table.update(words_tb)
    print('Words added to table')

    #lens = {len(rows) for col, rows in table.items()}
    #print(lens)
    
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

    requests_sample = sample(requests, 500)
    table = make_table(requests_sample)
    save(table)
    print('pickle saved')
    save(table, f_type = 'json')
    print('json saved')
    #df = pd.DataFrame(make_table(requests))
    #print(df.head())
    # }}}

main()
