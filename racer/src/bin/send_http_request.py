#!/usr/bin/env python

import os
import sys
from StringIO import StringIO
from BaseHTTPServer import BaseHTTPRequestHandler

CPP_HTTP_TIMING_EXECUTABLE = './run_http_timing_client'

class ParseException(Exception):
    pass

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
        self.request_body = self.rfile.read()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

def parse_request(request_text):
    request = HTTPRequest(request_text)

    if request.error_code:
        raise ParseException(request.error_message)

    return (request.command, request.path, request.request_version, request.request_body, request.headers)

def usage():
    print "usage: %s target path_to_request real_time? cpu_id delay reps" % (sys.argv[0])
    print "eg: %s https://www.google.com:43562 ./request.txt 1 0 10 100" % (sys.argv[0])
    sys.exit(1)


def main():
    if len(sys.argv) != 7:
        usage()

    target = sys.argv[1]
    path_to_request = sys.argv[2]
    real_time = sys.argv[3]
    cpu_id = sys.argv[4]
    delay = sys.argv[5]
    reps = sys.argv[6]

    try:
        verb, path, version, body, headers = parse_request(open(path_to_request).read())

    except ParseException as e:
        print "unable to parse request: %s" % e

    args = [CPP_HTTP_TIMING_EXECUTABLE, target + path, verb, version, body, real_time, cpu_id, delay, reps]
    args.extend(headers)
    print "running %s, args %s" % (CPP_HTTP_TIMING_EXECUTABLE, args)
    os.execvp(CPP_HTTP_TIMING_EXECUTABLE, args)


if __name__ == '__main__':
    main()
