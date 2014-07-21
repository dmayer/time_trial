import re
import os.path
import logging
import lib.filters as filters

class TimingData:

    def __init__(self):
        self.data = []
        self.logger = logging.getLogger('time_trial')


    def load_from_csv(self, file):
        self.full_path = file
        self.file_name = os.path.basename(file)
        self.logger.info("Loading from " + file)


        data_file = open(file)
        self.parse_csv(data_file)

    def parse_csv(self, data):
        if data == None or data == "":
            return


        if isinstance(data, str):
            str_data = data.split('\n')
        else:
            str_data = data.decode(encoding="utf-8").split('\n')


        for f in str_data:
            if ";" in str(f):
                s = f.split(";")[0]
                ns = f.split(";")[1]
                if  ns is not None and ns != "":
                    ns = int(re.sub(r"\D","", ns))
                    s = int(re.sub(r"\D","", s))
                    self.data.append(s*1e9 + ns)


    def quantile(self, i):
        return filters.PercentileFilter().apply(self, i)

