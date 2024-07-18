from numpy import pi, sqrt, exp, log, e, Infinity


class memory(object):

    #Memory class represents a memory that contains traces and decays related to those traces."
    #Fields:
        #sof: speed of forgetting of memory
        #c: spacing coefficent of memory
        #traces: list of traces of memory
        #id: list of decay in order with each trace
    #traces must be added in order (might fix later)


    def __init__(self, sof, c, s = 0.3, F = 1) -> None:

        "Initializes memory"
        #sof: speed of forgetting of memory
        #c: spacing coefficent of memory

        self.sof = sof
        self.c = c
        self.traces = []
        self.id = []
        self.s = s
        self.F = F

    def set_traces(self, traces):

        "entirely replaces current traces with parameterized traces"
        #traces: traces to replace old traces

        self.traces = traces

        for trace in self.traces:
            self.id.append(self.trace_decay(trace))


    def add_trace(self, time):

        "Adds trace to memory traces."
        #time: time of trace to be added

        if self.traces.__contains__(time):
            raise Exception(f"{time} has already been added as a trace")
        self.traces.append(time)
        self.id.append(self.trace_decay(time))

    def trace_decay(self, time):

        "helper method for add_trace"

        if len(self.id) == 0:
            return self.sof
        
        nd = self.c * e**(self.get_actv(time)) + self.sof
    
        return nd
    
    def get_actv(self, time):
        

        "returns activation of time"
        #time that will have its activation returned

        if len(self.traces) == 0:
            return -(Infinity)

        sum = 0
        i = 0
        while i < len(self.traces) and self.traces[i] < time:
            sum += (time - self.traces[i]) ** (-1*self.id[i])
            i += 1
        actv = log(sum)
        return min(actv, 10)
    
    #latency?

    def get_resp_time_dis(self, time, t0 = 0.6):
        beta = sqrt(3) / (pi * self.s)
        alpha = e ** -(self.get_actv(time))
        prob = (beta / (self.F * alpha)) * (((time - t0) / (self.F * alpha)) ** (beta - 1))
        prob = prob / ((1 + ((self.F * (time - t0)) / (self.F * alpha)) ** beta) ** 2) 
        return prob

    
    def get_s(self): return self.s
    