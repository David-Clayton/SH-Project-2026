import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyneb as pn

def icf_s(Z, v):
    """ICF for sulphur as function of v (O+/(O+ + O2+)) and 
    metallicity from Isotov 2006"""

    conditions = [Z < 7.2, Z > 8.2]

    choices = [0.121*v + 0.511 + 0.161/v, 0.178*v +  0.610 + 0.153/v]

    return np.select(conditions, choices, default = 0.155*v + 0.849 + 0.062/v)

def icf_ne(Z, w):
    """ICF for neon as function of w (O2+/(O+ + O2+)) and 
    metallicity from Isotov 2006"""

    conditions = [Z < 7.2, Z > 8.2]

    choices = [-0.385*w + 1.365 + 0.022/w, -0.591*w + 0.927 + 0.546/w]

    return np.select(conditions, choices, default = -0.405*w + 1.382 + 0.021/w)

def icf_ariii_ariv(Z, v):
    """ICF for argon as function of v (O+/(O+ + O2+)) and 
    metallicity from Isotov 2006 when using both ArIII and ArIV"""

    conditions = [Z < 7.2, Z > 8.2]

    choices = [0.158*v + 0.958 + 0.004/v, 0.238*v + 0.931 + 0.004/v]

    return np.select(conditions, choices, default = 0.104*v + 0.980 + 0.001/v)

    
def icf_ariii(Z, v):
    """ICF for argon as function of v (O+/(O+ + O2+)) and 
    metallicity from Isotov 2006 when using just ArIII"""

    conditions = [Z < 7.2, Z > 8.2]

    choices = [0.278*v + 0.836 + 0.051/v, 0.517*v + 0.763 + 0.042/v]

    return np.select(conditions, choices, default = 0.285*v + 0.833 + 0.051/v)


def icf_fe(Z, v):
    """ICF for iron as function of v (O+/(O+ + O2+)) and 
    metallicity from Isotov 2006"""

    conditions = [Z < 7.2, Z > 8.2]

    choices = [0.036*v - 0.146 + 1.386/v, -1.377*v + 1.606 + 1.045/v]

    return np.select(conditions, choices, default = 0.301*v - 0.259 + 1.367/v)

def fix_nan_issues(array):
    """Replace missing data in the LzLCS dataset from -999.999 to nan"""
    array[array == -999.999] = np.nan
    return array

def CLASSY():
    """Derive the S/O, Ne/O, Ar/O and Fe/O abundance ratios of CLASSY
    and same them to arrays"""

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    S2 = pn.Atom("S", 2)
    S3 = pn.Atom("S", 3)
    Ar3 = pn.Atom("Ar", 3)
    Ar4 = pn.Atom("Ar", 4)
    Ne3 = pn.Atom("Ne", 3)
    Fe3 = pn.Atom("Fe", 3)

    diags = pn.Diagnostics()

    #CLASSY emission lines

    classy_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Extra Abundances\Final_CLASSY_EMISSION_LINES_David.xlsx"

    h_beta = pd.read_excel(classy_cel_filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()[0:45]

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

    ar_iv_4711 = pd.read_excel(classy_cel_filepath, usecols = "AF", skiprows = 0).to_numpy().flatten()[0:45]
    ar_iv_4741 = pd.read_excel(classy_cel_filepath, usecols = "AJ", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869 = pd.read_excel(classy_cel_filepath, usecols = "CR", skiprows = 0).to_numpy().flatten()[0:45]

    fe_iii_4658 = pd.read_excel(classy_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:45]

    #Emission lines errors

    h_beta_err_up = pd.read_excel(classy_cel_filepath, usecols = "AO", skiprows = 0).to_numpy().flatten()[0:45]

    o_ii_3727_err_up = pd.read_excel(classy_cel_filepath, usecols = "C", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729_err_up = pd.read_excel(classy_cel_filepath, usecols = "G", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320_err_up = pd.read_excel(classy_cel_filepath, usecols = "CC", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330_err_up = pd.read_excel(classy_cel_filepath, usecols = "CG", skiprows = 0).to_numpy().flatten()[0:45]

    o_iii_5007_err_up = pd.read_excel(classy_cel_filepath, usecols = "AW", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959_err_up = pd.read_excel(classy_cel_filepath, usecols = "AS", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363_err_up = pd.read_excel(classy_cel_filepath, usecols = "S", skiprows = 0).to_numpy().flatten()[0:45]

    s_ii_6717_err_up = pd.read_excel(classy_cel_filepath, usecols = "BU", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731_err_up = pd.read_excel(classy_cel_filepath, usecols = "BY", skiprows = 0).to_numpy().flatten()[0:45]

    s_iii_6312_err_up = pd.read_excel(classy_cel_filepath, usecols = "BI", skiprows = 0).to_numpy().flatten()[0:45]
    s_iii_9069_err_up = pd.read_excel(classy_cel_filepath, usecols = "CO", skiprows = 0).to_numpy().flatten()[0:45]

    ar_iii_7135_err_up = pd.read_excel(classy_cel_filepath, usecols = "CK", skiprows = 0).to_numpy().flatten()[0:45]

    ar_iv_4711_err_up = pd.read_excel(classy_cel_filepath, usecols = "AG", skiprows = 0).to_numpy().flatten()[0:45]
    ar_iv_4741_err_up = pd.read_excel(classy_cel_filepath, usecols = "AK", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869_err_up = pd.read_excel(classy_cel_filepath, usecols = "CS", skiprows = 0).to_numpy().flatten()[0:45]

    fe_iii_4658_err_up = pd.read_excel(classy_cel_filepath, usecols = "AA", skiprows = 0).to_numpy().flatten()[0:45]



    h_beta_err_down = pd.read_excel(classy_cel_filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:45]

    o_ii_3727_err_down = pd.read_excel(classy_cel_filepath, usecols = "D", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729_err_down = pd.read_excel(classy_cel_filepath, usecols = "H", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320_err_down = pd.read_excel(classy_cel_filepath, usecols = "CD", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330_err_down = pd.read_excel(classy_cel_filepath, usecols = "CH", skiprows = 0).to_numpy().flatten()[0:45]

    o_iii_5007_err_down = pd.read_excel(classy_cel_filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959_err_down = pd.read_excel(classy_cel_filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363_err_down = pd.read_excel(classy_cel_filepath, usecols = "T", skiprows = 0).to_numpy().flatten()[0:45]

    s_ii_6717_err_down = pd.read_excel(classy_cel_filepath, usecols = "BV", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731_err_down = pd.read_excel(classy_cel_filepath, usecols = "BZ", skiprows = 0).to_numpy().flatten()[0:45]

    s_iii_6312_err_down = pd.read_excel(classy_cel_filepath, usecols = "BJ", skiprows = 0).to_numpy().flatten()[0:45]
    s_iii_9069_err_down = pd.read_excel(classy_cel_filepath, usecols = "CP", skiprows = 0).to_numpy().flatten()[0:45]

    ar_iii_7135_err_down = pd.read_excel(classy_cel_filepath, usecols = "CL", skiprows = 0).to_numpy().flatten()[0:45]

    ar_iv_4711_err_down = pd.read_excel(classy_cel_filepath, usecols = "AH", skiprows = 0).to_numpy().flatten()[0:45]
    ar_iv_4741_err_down = pd.read_excel(classy_cel_filepath, usecols = "AL", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869_err_down = pd.read_excel(classy_cel_filepath, usecols = "CT", skiprows = 0).to_numpy().flatten()[0:45]

    fe_iii_4658_err_down = pd.read_excel(classy_cel_filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:45]

    
    h_beta_err = (h_beta_err_up + h_beta_err_down) / 2

    o_ii_3727_err = (o_ii_3727_err_up + o_ii_3727_err_down) / 2
    o_ii_3729_err = (o_ii_3729_err_up + o_ii_3729_err_down) / 2
    o_ii_7320_err = (o_ii_7320_err_up + o_ii_7320_err_down) / 2    
    o_ii_7330_err = (o_ii_7330_err_up + o_ii_7330_err_down) / 2

    o_iii_5007_err = (o_iii_5007_err_up + o_iii_5007_err_down) / 2
    o_iii_4959_err = (o_iii_4959_err_up + o_iii_4959_err_down) / 2
    o_iii_4363_err = (o_iii_4363_err_up + o_iii_4363_err_down) / 2

    s_ii_6717_err = (s_ii_6717_err_up + s_ii_6717_err_down) / 2
    s_ii_6731_err = (s_ii_6731_err_up + s_ii_6731_err_down) / 2

    s_iii_6312_err = (s_iii_6312_err_up + s_iii_6312_err_down) / 2
    s_iii_9069_err = (s_iii_9069_err_up + s_iii_9069_err_down) / 2

    ar_iii_7135_err = (ar_iii_7135_err_up + ar_iii_7135_err_down) / 2

    ar_iv_4711_err = (ar_iv_4711_err_up + ar_iv_4711_err_down) / 2
    ar_iv_4741_err = (ar_iv_4741_err_up + ar_iv_4741_err_down) / 2

    ne_iii_3869_err = (ne_iii_3869_err_up + ne_iii_3869_err_down) / 2

    fe_iii_4658_err = (fe_iii_4658_err_up + fe_iii_4658_err_down) / 2

    #Intensity ratios for abundances

    o_iii_abund = (o_iii_4959 + o_iii_5007) / h_beta
    o_ii_abund_prim = (o_ii_3727 + o_ii_3729) / h_beta
    o_ii_abund_second = (o_ii_7320 + o_ii_7330) / h_beta
    s_ii_abund = (s_ii_6717 + s_ii_6731) / h_beta
    s_iii_abund = (s_iii_6312 + s_iii_9069) / h_beta
    ar_iii_abund = ar_iii_7135 / h_beta
    ar_iv_abund = (ar_iv_4711 + ar_iv_4741) / h_beta
    ne_iii_abund = ne_iii_3869 / h_beta
    fe_iii_abund = fe_iii_4658 / h_beta

    #Errors on abundances

    o_iii_abund_err = o_iii_abund * np.sqrt(((o_iii_4959_err**2 + o_iii_5007_err**2) / (o_iii_5007 + o_iii_4959)**2) + (h_beta_err/h_beta)**2)
    o_ii_abund_prim_err = o_ii_abund_prim * np.sqrt(((o_ii_3727_err**2 + o_ii_3729_err**2) / (o_ii_3727 + o_ii_3729)**2) + (h_beta_err/h_beta)**2)
    o_ii_abund_second_err = o_ii_abund_second * np.sqrt(((o_ii_7320_err**2 + o_ii_7330_err**2) / (o_ii_7320 + o_ii_7330)**2) + (h_beta_err/h_beta)**2)
    s_ii_abund_err = s_ii_abund * np.sqrt(((s_ii_6717_err**2 + s_ii_6731_err**2) / (s_ii_6717 + s_ii_6731)**2) + (h_beta_err/h_beta)**2)
    s_iii_abund_err = s_iii_abund * np.sqrt(((s_iii_6312_err**2 + s_iii_9069_err**2) / (s_iii_6312 + s_iii_9069)**2) + (h_beta_err/h_beta)**2)
    ar_iii_abund_err = ar_iii_abund * np.sqrt((ar_iii_7135_err/ar_iii_7135) ** 2 + (h_beta_err/h_beta) ** 2)
    ar_iv_abund_err = ar_iv_abund * np.sqrt(((ar_iv_4711_err**2 + ar_iv_4741_err**2) / (ar_iv_4711 + ar_iv_4741)**2) + (h_beta_err/h_beta)**2)
    ne_iii_abund_err = ne_iii_abund * np.sqrt((ne_iii_3869_err/ne_iii_3869) ** 2 + (h_beta_err/h_beta) ** 2)
    fe_iii_abund_err = fe_iii_abund * np.sqrt((fe_iii_4658_err/fe_iii_4658) ** 2 + (h_beta_err/h_beta) ** 2)

    #Intensity ratios for physical conditions

    o_iii_temp = o_iii_4363 / o_iii_5007
    s_iii_temp = s_iii_6312 / s_iii_9069
    o_ii_temp = (o_ii_3727 + o_ii_3729) / (o_ii_7320 + o_ii_7330)
    s_ii_dens = s_ii_6731 / s_ii_6717

    #Errors on physical conditions

    o_iii_temp_err = o_iii_temp * np.sqrt((o_iii_4363_err / o_iii_4363) ** 2 + (o_iii_5007_err / o_iii_5007) ** 2)
    s_iii_temp_err = s_iii_temp * np.sqrt((s_iii_6312_err / s_iii_6312) ** 2 + (s_iii_9069_err / s_iii_9069) ** 2)

    first_term = (o_ii_3727_err ** 2 + o_ii_3729_err ** 2) / ((o_ii_3727 + o_ii_3729) ** 2)
    second_term = (o_ii_7320_err ** 2 + o_ii_7330_err ** 2) / ((o_ii_7320 + o_ii_7330) ** 2)
    o_ii_temp_err = o_ii_temp * np.sqrt(first_term + second_term)

    s_ii_dens_err = s_ii_dens * np.sqrt((s_ii_6717_err / s_ii_6717) ** 2 + (s_ii_6731_err / s_ii_6731) ** 2)

    #Initial n_e sans errors
    n_e = diags.getCrossTemDen("[OIII] 4363/5007", "[SII] 6731/6716", o_iii_temp, s_ii_dens)[1]
    n_e = np.nan_to_num(n_e, nan = 100)

    #Temperatures in ionisation regions
    T_e_o_iii = O3.getTemDen(int_ratio = o_iii_temp, den = n_e, to_eval = "L(4363)/L(5007)")
    T_e_s_iii = S3.getTemDen(int_ratio = s_iii_temp, den = n_e, to_eval = "L(6312)/L(9069)")
    T_e_o_ii = O2.getTemDen(int_ratio = o_ii_temp, den = n_e, to_eval = "(L(3727)+L(3729))/(L(7320)+L(7330))")

    #Expand T[OII] and T[SIII] arrays with Garnett relations
    T_e_s_iii_exp = 0.83 * T_e_o_iii + 1700
    T_e_o_ii_exp = 0.7 * T_e_o_iii + 3000 

    #T_e_s_iii = np.where(np.isnan(T_e_s_iii), T_e_s_iii_exp, T_e_s_iii)
    #T_e_o_ii = np.where(np.isnan(T_e_o_ii), T_e_o_ii_exp, T_e_o_ii)

    T_e_s_iii = T_e_s_iii_exp
    T_e_o_ii = T_e_o_ii_exp

    #Raw abundances (i.e. without errors)

    OIII = O3.getIonAbundance(int_ratio = o_iii_abund, tem = T_e_o_iii, den = n_e, to_eval = "L(4959)+L(5007)", Hbeta = 1)
    OII_prim = O2.getIonAbundance(int_ratio = o_ii_abund_prim, tem = T_e_o_ii, den = n_e, to_eval = "L(3727)+L(3729)", Hbeta = 1)
    OII_second = O2.getIonAbundance(int_ratio = o_ii_abund_second, tem = T_e_o_ii, den = n_e, to_eval = "L(7320)+L(7330)", Hbeta = 1)
    SII = S2.getIonAbundance(int_ratio = s_ii_abund, tem = T_e_o_ii, den = n_e, to_eval = "L(6717)+L(6731)", Hbeta = 1)
    SIII = S3.getIonAbundance(int_ratio = s_iii_abund, tem = T_e_s_iii, den = n_e, to_eval = "L(6312)+L(9069)", Hbeta = 1)
    ArIII = Ar3.getIonAbundance(int_ratio = ar_iii_abund, tem = T_e_s_iii, den = n_e, to_eval = "L(7135)", Hbeta = 1)
    ArIV = Ar4.getIonAbundance(int_ratio = ar_iv_abund, tem = T_e_o_iii, den = n_e, to_eval = "L(4711)+L(4741)", Hbeta = 1)
    NeIII = Ne3.getIonAbundance(int_ratio = ne_iii_abund, tem = T_e_o_iii, den = n_e, to_eval = "L(3869)", Hbeta = 1)
    FeIII = Fe3.getIonAbundance(int_ratio = fe_iii_abund, tem = T_e_o_ii, den = n_e, to_eval = "L(4658)", Hbeta = 1)

    #Fill in empty O+ abundances with abundance prediction from secondary diagnostic
    OII = np.where(np.isnan(OII_prim), OII_second, OII_prim)

    #Ionisation parameters for ICFs
    v = OII/(OIII + OII)
    w = OIII/(OIII + OII)

    #Metallicity
    O = OII + OIII
    Z = 12 + np.log10(O)
    
    #Elemental abundances relative to oxygen
    S_O = ((SII + SIII)/(OII + OIII)) * icf_s(Z = Z, v = v)
    Ne_O = (NeIII / OIII) * icf_ne(Z = Z, w = w)
    Fe_O = (FeIII / OII) * icf_fe(Z = Z, v = v)
    #Argon with and without ArIV
    Ar_O_with = ((ArIII + ArIV) / OIII) * icf_ariii_ariv(Z = Z, v = v)
    Ar_O_without = (ArIII / OIII) * icf_ariii(Z = Z, v = v)
    #Use ArIII only measurements when ArIII + ArIV measurments fail
    Ar_O = np.where(np.isnan(Ar_O_with), Ar_O_without, Ar_O_with)

    #Get errors on abundances avec Monte Carlo

    #Empty arrays to store datums

    oii_mc_err_up = np.zeros(45)
    oii_mc_err_down = np.zeros(45)

    oiii_mc_err_up = np.zeros(45)
    oiii_mc_err_down = np.zeros(45)

    sii_mc_err_up = np.zeros(45)
    sii_mc_err_down = np.zeros(45)

    siii_mc_err_up = np.zeros(45)
    siii_mc_err_down = np.zeros(45)

    ariii_mc_err_up = np.zeros(45)
    ariii_mc_err_down = np.zeros(45)

    ariv_mc_err_up = np.zeros(45)
    ariv_mc_err_down = np.zeros(45)

    neiii_mc_err_up = np.zeros(45)
    neiii_mc_err_down = np.zeros(45)

    feiii_mc_err_up = np.zeros(45)
    feiii_mc_err_down = np.zeros(45)

    #Iterate over each galaxy

    for i in range(45):

        #Gaussian distributions for intensities
        oii_dist_prim = np.random.normal(o_ii_abund_prim[i], o_ii_abund_prim_err[i], size = 300)
        oii_dist_second = np.random.normal(o_ii_abund_second[i], o_ii_abund_second_err[i], size = 300)
        oiii_dist = np.random.normal(o_iii_abund[i], o_iii_abund_err[i], size = 300)
        sii_dist = np.random.normal(s_ii_abund[i], s_ii_abund_err[i], size = 300)
        siii_dist = np.random.normal(s_iii_abund[i], s_iii_abund_err[i], size = 300)
        ariii_dist = np.random.normal(ar_iii_abund[i], ar_iii_abund_err[i], size = 300)
        ariv_dist = np.random.normal(ar_iv_abund[i], ar_iv_abund_err[i], size = 300)
        neiii_dist = np.random.normal(ne_iii_abund[i], ne_iii_abund_err[i], size = 300)
        feiii_dist = np.random.normal(fe_iii_abund[i], fe_iii_abund_err[i], size = 300)

        #Turn scalars into arrays to match Gaussian dist length for PyNeb
        T_e_o_ii_array = np.full(300, T_e_o_ii[i])
        T_e_o_iii_array = np.full(300, T_e_o_iii[i])
        T_e_s_iii_array = np.full(300, T_e_s_iii[i])
        n_e_array = np.full(300, n_e[i])

        oii_abund_dist_prim = O2.getIonAbundance(oii_dist_prim, tem = T_e_o_ii_array, den = n_e_array, to_eval = "L(3727)+L(3729)", Hbeta = 1)
        oii_abund_dist_second = O2.getIonAbundance(oii_dist_second, tem = T_e_o_ii_array, den = n_e_array, to_eval = "L(7320)+L(7330)", Hbeta = 1)
        oiii_abund_dist = O3.getIonAbundance(oiii_dist, tem = T_e_o_iii_array, den = n_e_array, to_eval = "L(4959)+L(5007)", Hbeta = 1)
        sii_abund_dist = S2.getIonAbundance(sii_dist, tem = T_e_o_ii_array, den = n_e_array, to_eval = "L(6717)+L(6731)", Hbeta = 1)
        siii_abund_dist = S3.getIonAbundance(siii_dist, tem = T_e_s_iii_array, den = n_e_array, to_eval = "L(6312)+L(9069)", Hbeta = 1)
        ariii_abund_dist = Ar3.getIonAbundance(ariii_dist, tem = T_e_s_iii_array, den = n_e_array, to_eval = "L(7135)", Hbeta = 1)
        ariv_abund_dist = Ar4.getIonAbundance(ariv_dist, tem = T_e_o_iii_array, den = n_e_array, to_eval = "L(4711)+L(4741)", Hbeta = 1)
        neiii_abund_dist = Ne3.getIonAbundance(neiii_dist, tem = T_e_o_iii_array, den = n_e_array, to_eval = "L(3869)", Hbeta = 1)
        feiii_abund_dist = Fe3.getIonAbundance(feiii_dist, tem = T_e_o_ii_array, den = n_e_array, to_eval = "L(4658)", Hbeta = 1)
        oii_abund_dist = np.where(np.isnan(oii_abund_dist_prim), oii_abund_dist_prim, oii_abund_dist_second)

        #Medians and errors

        median_oii = np.nanmedian(oii_abund_dist)
        oii_err_up = np.nanpercentile(oii_abund_dist, 84) - median_oii
        oii_err_down = median_oii - np.nanpercentile(oii_abund_dist, 16)

        oii_mc_err_up[i] = oii_err_up
        oii_mc_err_down[i] = oii_err_down

        median_oiii = np.nanmedian(oiii_abund_dist)
        oiii_err_up = np.nanpercentile(oiii_abund_dist, 84) - median_oiii
        oiii_err_down = median_oiii - np.nanpercentile(oiii_abund_dist, 16)

        oiii_mc_err_up[i] = oiii_err_up
        oiii_mc_err_down[i] = oiii_err_down

        median_sii = np.nanmedian(sii_abund_dist)
        sii_err_up = np.nanpercentile(sii_abund_dist, 84) - median_sii
        sii_err_down = median_sii - np.nanpercentile(sii_abund_dist, 16)

        sii_mc_err_up[i] = sii_err_up
        sii_mc_err_down[i] = sii_err_down

        median_siii = np.nanmedian(siii_abund_dist)
        siii_err_up = np.nanpercentile(siii_abund_dist, 84) - median_siii
        siii_err_down = median_siii - np.nanpercentile(siii_abund_dist, 16)

        siii_mc_err_up[i] = siii_err_up
        siii_mc_err_down[i] = siii_err_down

        median_ariii = np.nanmedian(ariii_abund_dist)
        ariii_err_up = np.nanpercentile(ariii_abund_dist, 84) - median_ariii
        ariii_err_down = median_ariii - np.nanpercentile(ariii_abund_dist, 16)

        ariii_mc_err_up[i] = ariii_err_up
        ariii_mc_err_down[i] = ariii_err_down

        median_ariv = np.nanmedian(ariv_abund_dist)
        ariv_err_up = np.nanpercentile(ariv_abund_dist, 84) - median_ariv
        ariv_err_down = median_ariv - np.nanpercentile(ariv_abund_dist, 16)

        ariv_mc_err_up[i] = ariv_err_up
        ariv_mc_err_down[i] = ariv_err_down

        median_neiii = np.nanmedian(neiii_abund_dist)
        neiii_err_up = np.nanpercentile(neiii_abund_dist, 84) - median_neiii
        neiii_err_down = median_neiii - np.nanpercentile(neiii_abund_dist, 16)

        neiii_mc_err_up[i] = neiii_err_up
        neiii_mc_err_down[i] = neiii_err_down

        median_feiii = np.nanmedian(feiii_abund_dist)
        feiii_err_up = np.nanpercentile(feiii_abund_dist, 84) - median_feiii
        feiii_err_down = median_feiii - np.nanpercentile(feiii_abund_dist, 16)

        feiii_mc_err_up[i] = feiii_err_up
        feiii_mc_err_down[i] = feiii_err_down

        print(f"Error propagation for CLASSY galaxy {i+1}/45 complete.")


    #Propagate errors

    O_err_up = np.sqrt(oii_mc_err_up**2 + oiii_mc_err_up**2)
    O_err_down = np.sqrt(oiii_mc_err_down**2 + oiii_mc_err_down**2)

    Z = Z
    Z_err_up = O_err_up / (np.log(10) * O)
    Z_err_down = O_err_down / (np.log(10) * O)

    S = SII + SIII

    S_err_up = np.sqrt(sii_mc_err_up**2 + siii_mc_err_up**2)
    S_err_down = np.sqrt(sii_mc_err_down**2 + siii_mc_err_down**2)

    S_O_err_up = S_O * np.sqrt((S_err_up / S) ** 2 + (O_err_up / O) ** 2)
    S_O_err_down = S_O * np.sqrt((S_err_down / S) ** 2 + (O_err_down / O) ** 2)

    log_S_O = np.log10(S_O)
    log_S_O_err_up = S_O_err_up / (np.log(10) * S_O)
    log_S_O_err_down = S_O_err_down / (np.log(10) * S_O)

    Ar_with_IV = ArIII + ArIV
    Ar_with_IV_err_up = np.sqrt(ariii_mc_err_up ** 2 + ariv_mc_err_up ** 2)
    Ar_with_IV_err_down = np.sqrt(ariii_mc_err_down ** 2 + ariv_mc_err_down ** 2)

    Ar_O_with_err_up = Ar_O_with * np.sqrt((Ar_with_IV_err_up / Ar_with_IV) ** 2 + (oiii_mc_err_up / OIII) ** 2)
    Ar_O_with_err_down = Ar_O_with * np.sqrt((Ar_with_IV_err_down / Ar_with_IV) ** 2 + (oiii_mc_err_down / OIII) ** 2)

    Ar_O_without_err_up = Ar_O_without * np.sqrt((ariii_mc_err_up / ArIII) ** 2 + (oiii_mc_err_up / OIII) ** 2)
    Ar_O_without_err_down = Ar_O_without * np.sqrt((ariii_mc_err_down / ArIII) ** 2 + (oiii_mc_err_down / OIII) ** 2)

    Ar_O_err_up = np.where(np.isnan(Ar_O_with_err_up), Ar_O_without_err_up, Ar_O_with_err_up)   
    Ar_O_err_down = np.where(np.isnan(Ar_O_with_err_down), Ar_O_without_err_down, Ar_O_with_err_down)

    log_Ar_O = np.log10(Ar_O)
    log_Ar_O_err_up = Ar_O_err_up / (np.log(10) * Ar_O)
    log_Ar_O_err_down = Ar_O_err_down / (np.log(10) * Ar_O)

    Ne_O_err_up = Ne_O * np.sqrt((neiii_mc_err_up / NeIII) ** 2 + (oiii_mc_err_up / OIII) ** 2)
    Ne_O_err_down = Ne_O * np.sqrt((neiii_mc_err_down / NeIII) ** 2 + (oiii_mc_err_down / OIII) ** 2)

    log_Ne_O = np.log10(Ne_O)
    log_Ne_O_err_up = Ne_O_err_up / (np.log(10) * Ne_O)
    log_Ne_O_err_down = Ne_O_err_down / (np.log(10) * Ne_O)

    Fe_O_err_up = Fe_O * np.sqrt((feiii_mc_err_up / FeIII) ** 2 + (oii_mc_err_up / OII) ** 2)
    Fe_O_err_down = Fe_O * np.sqrt((feiii_mc_err_down / FeIII) ** 2 + (oii_mc_err_down / OII) ** 2)

    log_Fe_O = np.log10(Fe_O)
    log_Fe_O_err_up = Fe_O_err_up / (np.log(10) * Fe_O)
    log_Fe_O_err_down = Fe_O_err_down / (np.log(10) * Fe_O)

    #Save data to CSV with physical conditions data

    classy_phys_cond_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Extra Abundances\classy_sample_prop.csv"
    mass = pd.read_csv(classy_phys_cond_filepath, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()[0:45]
    sfr = pd.read_csv(classy_phys_cond_filepath, delimiter = ",", usecols = [7], header = 0).to_numpy().flatten()[0:45]

    data = np.column_stack((mass, sfr, Z, Z_err_up, Z_err_down, log_S_O, log_S_O_err_up, log_S_O_err_down, log_Ar_O, log_Ar_O_err_up, log_Ar_O_err_down, log_Ne_O, log_Ne_O_err_up, log_Ne_O_err_down, log_Fe_O, log_Fe_O_err_up, log_Fe_O_err_down))
    np.savetxt("classyextras.csv", data, delimiter = ",", header = "mass, sfr, Z, Z_err_up, Z_err_down, log_S_O, log_S_O_err_up, log_S_O_err_down, log_Ar_O, log_Ar_O_err_up, log_Ar_O_err_down, log_Ne_O, log_Ne_O_err_up, log_Ne_O_err_down, log_Fe_O, log_Fe_O_err_up, log_Fe_O_err_down")

def LzLCS():

    """Derive the S/O, Ne/O, Ar/O and Fe/O abundance ratios of LzLCS
    and same them to arrays"""

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    S2 = pn.Atom("S", 2)
    Ne3 = pn.Atom("Ne", 3)
    diags = pn.Diagnostics()

    #LzLCS emission lines

    lzlcs_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Extra Abundances\Final_LYC_EMISSION_LINES_David.xlsx"

    h_beta = pd.read_excel(lzlcs_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:27]

    o_ii_3727 = pd.read_excel(lzlcs_cel_filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3729 = pd.read_excel(lzlcs_cel_filepath, usecols = "L", skiprows = 0).to_numpy().flatten()[0:27]

    o_iii_5007 = pd.read_excel(lzlcs_cel_filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4959 = pd.read_excel(lzlcs_cel_filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4363 = pd.read_excel(lzlcs_cel_filepath, usecols = "V", skiprows = 0).to_numpy().flatten()[0:27]

    s_ii_6717 = pd.read_excel(lzlcs_cel_filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:27]
    s_ii_6731 = pd.read_excel(lzlcs_cel_filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:27]

    ne_iii_3869 = pd.read_excel(lzlcs_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:27]

    #Emission lines errors

    h_beta_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AA", skiprows = 0).to_numpy().flatten()[0:27]

    o_ii_3727_err = pd.read_excel(lzlcs_cel_filepath, usecols = "K", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3729_err = pd.read_excel(lzlcs_cel_filepath, usecols = "M", skiprows = 0).to_numpy().flatten()[0:27]
   
    o_iii_5007_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AE", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4959_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AC", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4363_err = pd.read_excel(lzlcs_cel_filepath, usecols = "W", skiprows = 0).to_numpy().flatten()[0:27]

    s_ii_6717_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AS", skiprows = 0).to_numpy().flatten()[0:27]
    s_ii_6731_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AU", skiprows = 0).to_numpy().flatten()[0:27]

    ne_iii_3869_err = pd.read_excel(lzlcs_cel_filepath, usecols = "O", skiprows = 0).to_numpy().flatten()[0:27]

    #Fix nan issues

    h_beta = fix_nan_issues(h_beta)
    o_ii_3727 = fix_nan_issues(o_ii_3727)
    o_ii_3729 = fix_nan_issues(o_ii_3729)
    o_iii_5007 = fix_nan_issues(o_iii_5007)
    o_iii_4959 = fix_nan_issues(o_iii_4959)
    o_iii_4363 = fix_nan_issues(o_iii_4363)
    s_ii_6717 = fix_nan_issues(s_ii_6717)
    s_ii_6731 = fix_nan_issues(s_ii_6731)
    ne_iii_3869 = fix_nan_issues(ne_iii_3869)

    h_beta_err = fix_nan_issues(h_beta_err)
    o_ii_3727_err = fix_nan_issues(o_ii_3727_err)
    o_ii_3729_err = fix_nan_issues(o_ii_3729_err)
    o_iii_5007_err = fix_nan_issues(o_iii_5007_err)
    o_iii_4959_err = fix_nan_issues(o_iii_4959_err)
    o_iii_4363_err = fix_nan_issues(o_iii_4363_err)
    s_ii_6717_err = fix_nan_issues(s_ii_6717_err)
    s_ii_6731_err = fix_nan_issues(s_ii_6731_err)
    ne_iii_3869_err = fix_nan_issues(ne_iii_3869_err)

    #Intensity ratios for abundances

    o_iii_abund = (o_iii_4959 + o_iii_5007) / h_beta
    o_ii_abund = (o_ii_3727 + o_ii_3729) / h_beta
    s_ii_abund = (s_ii_6717 + s_ii_6731) / h_beta
    ne_iii_abund = ne_iii_3869 / h_beta

    #Errors on abundances

    o_iii_abund_err = o_iii_abund * np.sqrt(((o_iii_4959_err**2 + o_iii_5007_err**2) / (o_iii_5007 + o_iii_4959)**2) + (h_beta_err/h_beta)**2)
    o_ii_abund_err = o_ii_abund * np.sqrt(((o_ii_3727_err**2 + o_ii_3729_err**2) / (o_ii_3727 + o_ii_3729)**2) + (h_beta_err/h_beta)**2)
    s_ii_abund_err = s_ii_abund * np.sqrt(((s_ii_6717_err**2 + s_ii_6731_err**2) / (s_ii_6717 + s_ii_6731)**2) + (h_beta_err/h_beta)**2)
    ne_iii_abund_err = ne_iii_abund * np.sqrt((ne_iii_3869_err/ne_iii_3869) ** 2 + (h_beta_err/h_beta) ** 2)
   
    #Intensity ratios for physical conditions

    o_iii_temp = o_iii_4363 / o_iii_5007
    #No emission lines for o_ii_temp 
    s_ii_dens = s_ii_6731 / s_ii_6717

    #Errors on physical conditions

    o_iii_temp_err = o_iii_temp * np.sqrt((o_iii_4363_err / o_iii_4363) ** 2 + (o_iii_5007_err / o_iii_5007) ** 2)

    s_ii_dens_err = s_ii_dens * np.sqrt((s_ii_6717_err / s_ii_6717) ** 2 + (s_ii_6731_err / s_ii_6731) ** 2)

    #Initial n_e sans errors
    n_e = diags.getCrossTemDen("[OIII] 4363/5007", "[SII] 6731/6716", o_iii_temp, s_ii_dens)[1]
    n_e = np.nan_to_num(n_e, nan = 100)

    #Temperatures in ionisation regions
    T_e_o_iii = O3.getTemDen(int_ratio = o_iii_temp, den = n_e, to_eval = "L(4363)/L(5007)")

    #Expand T[OII] and T[SIII] arrays with Garnett relations
    T_e_s_iii = 0.83 * T_e_o_iii + 1700
    T_e_o_ii = 0.7 * T_e_o_iii + 3000 

    #Raw abundances (i.e. without errors)

    OIII = O3.getIonAbundance(int_ratio = o_iii_abund, tem = T_e_o_iii, den = n_e, to_eval = "L(4959)+L(5007)", Hbeta = 1)
    OII = O2.getIonAbundance(int_ratio = o_ii_abund, tem = T_e_o_ii, den = n_e, to_eval = "L(3727)+L(3729)", Hbeta = 1)
    SII = S2.getIonAbundance(int_ratio = s_ii_abund, tem = T_e_o_ii, den = n_e, to_eval = "L(6717)+L(6731)", Hbeta = 1)
    NeIII = Ne3.getIonAbundance(int_ratio = ne_iii_abund, tem = T_e_o_iii, den = n_e, to_eval = "L(3869)", Hbeta = 1)

    #Ionisation parameters for ICFs
    v = OII/(OIII + OII)
    w = OIII/(OIII + OII)

    #Metallicity
    O = OII + OIII
    Z = 12 + np.log10(O)
    
    #Elemental abundances relative to oxygen
    Ne_O = (NeIII / OIII) * icf_ne(Z = Z, w = w)

    #Get errors on abundances avec Monte Carlo

    #Empty arrays to store datums

    oii_mc_err_up = np.zeros(27)
    oii_mc_err_down = np.zeros(27)

    oiii_mc_err_up = np.zeros(27)
    oiii_mc_err_down = np.zeros(27)

    sii_mc_err_up = np.zeros(27)
    sii_mc_err_down = np.zeros(27)

    neiii_mc_err_up = np.zeros(27)
    neiii_mc_err_down = np.zeros(27)

    #Iterate over each galaxy

    for i in range(27):

        #Gaussian distributions for intensities
        oii_dist = np.random.normal(o_ii_abund[i], o_ii_abund_err[i], size = 300)
        oiii_dist = np.random.normal(o_iii_abund[i], o_iii_abund_err[i], size = 300)
        sii_dist = np.random.normal(s_ii_abund[i], s_ii_abund_err[i], size = 300)
        neiii_dist = np.random.normal(ne_iii_abund[i], ne_iii_abund_err[i], size = 300)

        T_e_o_ii_array = np.full(300, T_e_o_ii[i])
        n_e_array = np.full(300, n_e[i])
        T_e_o_iii_array = np.full(300, T_e_o_iii[i])

        oii_abund_dist = O2.getIonAbundance(oii_dist, tem = T_e_o_ii_array, den = n_e_array, to_eval = "L(3727)+L(3729)", Hbeta = 1)
        oiii_abund_dist = O3.getIonAbundance(oiii_dist, tem = T_e_o_iii_array, den = n_e_array, to_eval = "L(4959)+L(5007)", Hbeta = 1)
        sii_abund_dist = S2.getIonAbundance(sii_dist, tem = T_e_o_ii_array, den = n_e_array, to_eval = "L(6717)+L(6731)", Hbeta = 1)
        neiii_abund_dist = Ne3.getIonAbundance(neiii_dist, tem = T_e_o_iii_array, den = n_e_array, to_eval = "L(3869)", Hbeta = 1)

        #Medians and errors

        median_oii = np.nanmedian(oii_abund_dist)
        oii_err_up = np.nanpercentile(oii_abund_dist, 84) - median_oii
        oii_err_down = median_oii - np.nanpercentile(oii_abund_dist, 16)

        oii_mc_err_up[i] = oii_err_up
        oii_mc_err_down[i] = oii_err_down

        median_oiii = np.nanmedian(oiii_abund_dist)
        oiii_err_up = np.nanpercentile(oiii_abund_dist, 84) - median_oiii
        oiii_err_down = median_oiii - np.nanpercentile(oiii_abund_dist, 16)

        oiii_mc_err_up[i] = oiii_err_up
        oiii_mc_err_down[i] = oiii_err_down

        median_sii = np.nanmedian(sii_abund_dist)
        sii_err_up = np.nanpercentile(sii_abund_dist, 84) - median_sii
        sii_err_down = median_sii - np.nanpercentile(sii_abund_dist, 16)

        sii_mc_err_up[i] = sii_err_up
        sii_mc_err_down[i] = sii_err_down

        median_neiii = np.nanmedian(neiii_abund_dist)
        neiii_err_up = np.nanpercentile(neiii_abund_dist, 84) - median_neiii
        neiii_err_down = median_neiii - np.nanpercentile(neiii_abund_dist, 16)

        neiii_mc_err_up[i] = neiii_err_up
        neiii_mc_err_down[i] = neiii_err_down

        print(f"Error propagation for LzLCS galaxy {i+1}/27 complete.")


    #Propagate errors

    O_err_up = np.sqrt(oii_mc_err_up**2 + oiii_mc_err_up**2)
    O_err_down = np.sqrt(oiii_mc_err_down**2 + oiii_mc_err_down**2)

    Z = Z
    Z_err_up = O_err_up / (np.log(10) * O)
    Z_err_down = O_err_down / (np.log(10) * O)

    Ne_O_err_up = Ne_O * np.sqrt((neiii_mc_err_up / NeIII) ** 2 + (oiii_mc_err_up / OIII) ** 2)
    Ne_O_err_down = Ne_O * np.sqrt((neiii_mc_err_down / NeIII) ** 2 + (oiii_mc_err_down / OIII) ** 2)

    log_Ne_O = np.log10(Ne_O)
    log_Ne_O_err_up = Ne_O_err_up / (np.log(10) * Ne_O)
    log_Ne_O_err_down = Ne_O_err_down / (np.log(10) * Ne_O)

    #Save data to CSV with physical conditions data

    lzlcs_sfr_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Extra Abundances\SFR.csv"
    mass = pd.read_excel(lzlcs_cel_filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:27]
    mass_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AY", skiprows = 0).to_numpy().flatten()[0:27]
    sfr = pd.read_csv(lzlcs_sfr_filepath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()[0:27]
    sfr_err = pd.read_csv(lzlcs_sfr_filepath, delimiter = ",", usecols = [3], header = 0).to_numpy().flatten()[0:27]

    data = np.column_stack((mass, mass_err, sfr, sfr_err, Z, Z_err_up, Z_err_down, log_Ne_O, log_Ne_O_err_up, log_Ne_O_err_down))
    np.savetxt("lzlcsextras.csv", data, delimiter = ",", header = "mass, mass_err, sfr, sfr_err, Z, Z_err_up, Z_err_down, log_Ne_O, log_Ne_O_err_up, log_Ne_O_err_down")

def main():
    CLASSY()
    LzLCS()

main()











