import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt

def nicholls2017(metallicity):
    """Relation to fit log(N/O) with 12+log(O/H)"""
    a = -1.732
    b = 2.19

    ratio = np.log10(10 ** a + 10 ** (metallicity -12 + b))
    return ratio

    

