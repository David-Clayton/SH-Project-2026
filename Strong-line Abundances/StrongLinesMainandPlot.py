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

def fix_nan_issues(array):
    """Replace missing data in the LzLCS dataset from -999.999 to nan"""
    array[array == -999.999] = np.nan
    return array

def CLASSY():
    #CLASSY emission lines

    classy_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\Final_CLASSY_EMISSION_LINES_David.xlsx"
    classy_data_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\classyextras.csv"

    names = pd.read_excel(classy_cel_filepath, usecols = "A", skiprows = 0).to_numpy().flatten()[0:45]

    h_beta = pd.read_excel(classy_cel_filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()[0:45]
    h_gamma = pd.read_excel(classy_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:45]

    o_ii_3727 = pd.read_excel(classy_cel_filepath, usecols = "B", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729 = pd.read_excel(classy_cel_filepath, usecols = "F", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320 = pd.read_excel(classy_cel_filepath, usecols = "CB", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330 = pd.read_excel(classy_cel_filepath, usecols = "CF", skiprows = 0).to_numpy().flatten()[0:45]

    o_iii_5007 = pd.read_excel(classy_cel_filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959 = pd.read_excel(classy_cel_filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363 = pd.read_excel(classy_cel_filepath, usecols = "R", skiprows = 0).to_numpy().flatten()[0:45]

    s_ii_6717 = pd.read_excel(classy_cel_filepath, usecols = "BT", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731 = pd.read_excel(classy_cel_filepath, usecols = "BX", skiprows = 0).to_numpy().flatten()[0:45]

    s_iii_6312 = pd.read_excel(classy_cel_filepath, usecols = "BH", skiprows = 0).to_numpy().flatten()[0:45]
    s_iii_9069 = pd.read_excel(classy_cel_filepath, usecols = "CN", skiprows = 0).to_numpy().flatten()[0:45]

    ar_iii_7135 = pd.read_excel(classy_cel_filepath, usecols = "CJ", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869 = pd.read_excel(classy_cel_filepath, usecols = "CR", skiprows = 0).to_numpy().flatten()[0:45]

    fe_iii_4658 = pd.read_excel(classy_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:45]

    #Direct method metallicity
    direct_Z = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()
    direct_Z_err_up = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [7], header = 0).to_numpy().flatten()
    direct_Z_err_down = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    direct_Z_err = (direct_Z_err_up + direct_Z_err_down) / 2


def LzLCS():
    #LzLCS emission lines

    lzlcs_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\Final_LYC_EMISSION_LINES_David.xlsx"
    lzlcs_data_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\lzlcsextras.csv"

    names = pd.read_excel(lzlcs_cel_filepath, usecols = "A", skiprows = 0).to_numpy().flatten()[0:27]

    h_beta = pd.read_excel(lzlcs_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:27]
    h_gamma = pd.read_excel(lzlcs_cel_filepath, usecols = "T", skiprows = 0).to_numpy().flatten()[0:27]

    o_ii_3727 = pd.read_excel(lzlcs_cel_filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3729 = pd.read_excel(lzlcs_cel_filepath, usecols = "L", skiprows = 0).to_numpy().flatten()[0:27]

    o_iii_5007 = pd.read_excel(lzlcs_cel_filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4959 = pd.read_excel(lzlcs_cel_filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4363 = pd.read_excel(lzlcs_cel_filepath, usecols = "V", skiprows = 0).to_numpy().flatten()[0:27]

    s_ii_6717 = pd.read_excel(lzlcs_cel_filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:27]
    s_ii_6731 = pd.read_excel(lzlcs_cel_filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:27]

    ne_iii_3869 = pd.read_excel(lzlcs_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:27]

    h_beta = fix_nan_issues(h_beta)
    o_ii_3727 = fix_nan_issues(o_ii_3727)
    o_ii_3729 = fix_nan_issues(o_ii_3729)
    o_iii_5007 = fix_nan_issues(o_iii_5007)
    o_iii_4959 = fix_nan_issues(o_iii_4959)
    o_iii_4363 = fix_nan_issues(o_iii_4363)
    s_ii_6717 = fix_nan_issues(s_ii_6717)
    s_ii_6731 = fix_nan_issues(s_ii_6731)
    ne_iii_3869 = fix_nan_issues(ne_iii_3869)

    #Direct method metallicity
    direct_Z = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    direct_Z_err_up = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [9], header = 0).to_numpy().flatten()
    direct_Z_err_down = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [10], header = 0).to_numpy().flatten()
    direct_Z_err = (direct_Z_err_up + direct_Z_err_down) / 2