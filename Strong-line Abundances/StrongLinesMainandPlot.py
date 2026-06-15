import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt

def metallicity(a_0, a_1, a_2, a_3, x):
    """Derive the metallicity from the polynomial parameterisation of strong line intensity ratios (x)
    given by Eq. 2 in Rosales-Ortega et al. (2026) for the case of HII regions having imhomogeneous
    temperature structures (t^2 > 0)"""

    Z = a_0 + (a_1 * x) * (a_2 * x**2) + (a_3 * x**3)

    return Z

def error(e_0, e_1, e_2, x):
    """Derive the polynomial parameterisation of the dispersion (sigma) from the strong line 
    ratios, where the error on the metallicity is given as 1*sigma"""

    sigma = e_0 + (e_1 * x) + (e_2 * x**2)

    return sigma

