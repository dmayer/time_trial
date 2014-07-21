

class Plot:

    def __init__(self, timing_data, label = "Data"):
        self.timing_data = timing_data
        self.label = label
        self.color = "red"
        self.bins = 25
        self.style = "stepfilled"
        self.style_types = {'bar' : "Bar",
                            'step' : "Step",
                            'stepfilled' : "Step - Filled"}
        self.minimum = 0
        self.maximum = 99
        self.range_type = "percentile"


    def style_name(self):
        return self.style_types[self.style]
