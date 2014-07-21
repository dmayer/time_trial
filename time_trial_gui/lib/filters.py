import numpy as np

class PercentileFilter:

    def __init__(self):
        pass

    def apply(self, timing_data, percentile):
        np_data = np.array(timing_data.data)
        return np.percentile(np_data, percentile)