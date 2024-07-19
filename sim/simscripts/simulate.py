from slimstampen.spacingmodel import SpacingModel, Fact, Response
import matplotlib.pyplot as plt 
from numpy import pi, sqrt, exp, log, e, Infinity
import numpy as np
import random as r
from memory import memory
from scipy.stats import logistic
import pandas as pd

 #minutes
FORGET_THRESHOLD = -0.8
q_buff = 0.6

#Returns a random activation based off of the determinstic eq and the logistic distribution of activation.
# m: Memory to calculate random activation of
# t: time in which activation will be measured
def noise_actv(m, t):
    sd = pi * m.get_s()/ sqrt(3)
    noisedist = logistic(m.get_actv(t), sd)
    new_actv = noisedist.rvs()
    return new_actv

#Returns aresponse time based off of the deterministic eq for response time and activation
#actv: Activation of memory
#t0: Reaction time buffer, basically the minimum resposnse time
def calc_rst(actv, F, t0):
    return t0 + F * (e ** (- actv))


#Returns a true or false response based off the activation, the s parameter, and our determined activation threshold (What is the actv thresh?)
def get_response(actv, s, thresh):
    prob = 1 / (1 + e ** (-(actv - thresh) / s))
    resp = r.uniform(0, 1) <= prob
    return resp


def simulate(sm, SIM_END_TIME, NUM_FACTS, SOF, c = 0.25, S = 0.3, F = 1, t0 = 0.3):

    "Runs a MemoryLab session using a ACT-R Memory model for each fact. Returns speed of forgetting for each fact presented"
    "Parameters:"
    "sm: passed spacingmodel"
    "SIM_END_TIME: How long memory Lab session lasts"
    "NUM_FACTS: Number of facts that could be presented"
    "SOF: Speed of forgetting of the 'testee'"
    "c: Spacing coefficient for decay"
    "s: noise parameter for activation"
    "F: Parameter in response probability"
    "t0: reaction time of 'testee'"
    "returns: Dataframe of question sofs and following parameters"

    t = 0
    sm = SpacingModel()

    memories = []

    for x in range(NUM_FACTS):
        fact = Fact(x, "q", "q")
        sm.add_fact(fact)
        memories.append(memory(SOF, c, s=S, F=F))

    while t <= SIM_END_TIME * 60:
        fact, new = sm.get_next_fact(t * 1000)

        if new:
            #IF FACT IS NEW, ADD CREATE FACT MEMORY, PLEASE ASK ANDREA ABOUT THIS
            #Okay so the way its currently set up, I get -infinity when t = encoding time, but should be infinity at that time no?
            #Im gonna do it ask andrea abti it l8r
            
            fact_id = fact.fact_id
            memories[fact_id].add_trace(t)
            actv = Infinity                         #PLEASSE COME BACK TO THIS
            corr = get_response(actv, S, FORGET_THRESHOLD)
            rst = calc_rst(actv, F, t0) # for milliseconds

            t += rst

            resp = Response(fact, t * 1000, rst * 1000, corr)
            sm.register_response(resp)

            t += q_buff

        else:
            fact_id = fact[0]
            actv = noise_actv(memories[fact_id], t)
            corr = get_response(actv, S, FORGET_THRESHOLD)
            rst = calc_rst(actv, F, t0)

            resp = Response(fact, t * 1000, rst * 1000, corr)
            sm.register_response(resp)

            t += rst
            memories[fact_id].add_trace(t)
            
            if corr:
                t += q_buff
            else:
                t += 4
    
    sof = []
    for x in range(NUM_FACTS):
        sof.append(sm.get_rate_of_forgetting(t * 1000, sm.facts[x]))

    params = ["sim_time", "forget_threshold", "num_facts", "model_sof", "c", "s", "F", "t0"]
    sof.extend([SIM_END_TIME, FORGET_THRESHOLD, NUM_FACTS, SOF, c, S, F, t0])
    col = [f"Q{x}" for x in range(1, NUM_FACTS + 1)]
    col.extend(params)

    df = pd.DataFrame(np.array([sof]), columns = col)
    return df


if __name__ == "__main__":
    import datetime

    df = simulate(1, 20, 0.3) 
    print(df)
    for msof in [x / 100 for x in range(31, 50)]:
        df = pd.concat([df, simulate(1, 20, msof)], ignore_index=True)

    df.to_csv("dataanalysis\\data\\bobo")

