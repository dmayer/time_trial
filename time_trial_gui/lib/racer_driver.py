from http.server import BaseHTTPRequestHandler
from io import StringIO, BytesIO
import os

__author__ = 'daniel'

CPP_HTTP_TIMING_EXECUTABLE = '../../../../cpp/bin/run_http_timing_client'
CPP_ECHO_TIMING_EXECUTABLE = "/home/mayer/repos/remote_timing_attacks/src/cpp/bin/run_timing_client"


import subprocess


class ParseException(Exception):
    pass

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = BytesIO(request_text)
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

    # request.headers is still a message object
    # items returns a list of tuples, but we need actual header k,v pairs:
    header_list = [x[0] + ": " + x[1] for x in request.headers.items()]

    return (request.command, request.path, request.request_version, request.request_body, header_list )




def execute_trial(trial):
    cmd = []

    if trial.__class__.__name__ == "HTTPTrialJob":
        print("Executing HTTP Trial...")
        print(repr(trial.request))

        try:
            verb, path, version, body, headers = parse_request(bytes(trial.request,"iso-8859-1"))

        except ParseException as e:
            print("unable to parse request: %s" % e)

        cmd = [CPP_HTTP_TIMING_EXECUTABLE, trial.request_url + path, verb, version, body, str(trial.real_time), str(trial.core_affinity), " ", str(trial.reps)]
        cmd.extend(headers)
        print("running %s, args %s" % (CPP_HTTP_TIMING_EXECUTABLE, cmd))

    else:
        print("Executing Echo Trial...")
        #TODO: get this from a config file
        cmd.append("/home/mayer/repos/remote_timing_attacks/src/cpp/bin/run_timing_client")
        cmd.append(trial.target_host)
        cmd.append(str(trial.target_port))
        cmd.append(str(int(trial.real_time)))
        cmd.append(str(trial.core_affinity))
        cmd.append(str(trial.delay))
        cmd.append(str(trial.reps))
        print(cmd)

    return subprocess.check_output(cmd)



