import sys


with open(sys.argv[1]) as datafile:
    emptylines = 0
    newrequest = True
    for line in datafile:
        if line == '\n':
            emptylines += 1
            if emptylines == 2:
                newrequest = True
                emptylines = 0;
        else:
            if emptylines == 1:
                request_body = line
                #print(request_body)
            elif newrequest:
                request_type, request_url, request_version = line.split()
                file_and_parameters = request_url[21:]
                f = file_and_parameters.split('?')
                #print("%s %s %s" % (request_type, request_url, request_version))
                newrequest = False


