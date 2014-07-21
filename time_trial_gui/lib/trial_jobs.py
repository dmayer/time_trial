__author__ = 'daniel'

class TrialJob:
    def __init__(self):
        self.real_time = 1
        self.core_affinity = 1
        self.reps = 1



class EchoTrialJob(TrialJob):
    def __init__(self):
        TrialJob.__init__(self)
        # in nanoseconds (for now :-/)
        self.delay = 100
        self.target_host = ""
        self.target_port = ""


class HTTPTrialJob(TrialJob):
    def __init__(self):
        TrialJob.__init__(self)
        self.request_url = ""
        self.request = ""
