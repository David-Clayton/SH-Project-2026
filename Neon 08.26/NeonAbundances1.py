import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyneb as pn

def icf_ne(Z, w):
    """ICF for neon as function of w (O2+/(O+ + O2+)) and 
    metallicity from Isotov 2006"""

    conditions = [Z < 7.2, Z > 8.2]

    choices = [-0.385*w + 1.365 + 0.022/w, -0.591*w + 0.927 + 0.546/w]

    return np.select(conditions, choices, default = -0.405*w + 1.382 + 0.021/w)

def fix_nan_issues(array):
    """Replace missing data in the LzLCS dataset from -999.999 to nan"""
    array[array == -999.999] = np.nan
    return array


def LzLCS():

    """Derive the S/O, Ne/O, Ar/O and Fe/O abundance ratios of LzLCS
    and same them to arrays"""

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    S2 = pn.Atom("S", 2)
    Ne3 = pn.Atom("Ne", 3)
    diags = pn.Diagnostics()

    #LzLCS emission lines

    lzlcs_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Neon 08.26\Final_LYC_EMISSION_LINES_David.xlsx"

    names = pd.read_excel(lzlcs_cel_filepath, usecols = "A", skiprows = 0).to_numpy().flatten()[0:26]

    h_beta = pd.read_excel(lzlcs_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:26]

    o_ii_3727 = pd.read_excel(lzlcs_cel_filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:26]
    o_ii_3729 = pd.read_excel(lzlcs_cel_filepath, usecols = "L", skiprows = 0).to_numpy().flatten()[0:26]

    o_iii_4363 = pd.read_excel(lzlcs_cel_filepath, usecols = "V", skiprows = 0).to_numpy().flatten()[0:26]
    o_iii_4959 = pd.read_excel(lzlcs_cel_filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:26]
    o_iii_5007 = 2.98 * o_iii_4959 
    #This CEL is clipped in high-emission galaxies in the SDSS. 
    #Making use of a theoretical ratio between [OIII]5007 and [OIII]4959

    s_ii_6717 = pd.read_excel(lzlcs_cel_filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:26]
    s_ii_6731 = pd.read_excel(lzlcs_cel_filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:26]

    ne_iii_3869 = pd.read_excel(lzlcs_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:26]

    #Emission lines errors

    h_beta_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AA", skiprows = 0).to_numpy().flatten()[0:26]

    o_ii_3727_err = pd.read_excel(lzlcs_cel_filepath, usecols = "K", skiprows = 0).to_numpy().flatten()[0:26]
    o_ii_3729_err = pd.read_excel(lzlcs_cel_filepath, usecols = "M", skiprows = 0).to_numpy().flatten()[0:26]
   
    o_iii_4363_err = pd.read_excel(lzlcs_cel_filepath, usecols = "W", skiprows = 0).to_numpy().flatten()[0:26]
    o_iii_4959_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AC", skiprows = 0).to_numpy().flatten()[0:26]
    o_iii_5007_err = 2.98 * o_iii_4959_err

    s_ii_6717_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AS", skiprows = 0).to_numpy().flatten()[0:26]
    s_ii_6731_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AU", skiprows = 0).to_numpy().flatten()[0:26]

    ne_iii_3869_err = pd.read_excel(lzlcs_cel_filepath, usecols = "O", skiprows = 0).to_numpy().flatten()[0:26]

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

    #Metallicity
    O = OII + OIII
    Z = 12 + np.log10(O)

    #Ionisation parameters for ICFs
    w = OIII/(OIII + OII)

    #Elemental abundances relative to oxygen
    Ne_O = (NeIII / OIII) * icf_ne(Z = Z, w = w)

    #Get errors on abundances avec Monte Carlo

    #Empty arrays to store datums

    oii_mc_err_up = np.zeros(26)
    oii_mc_err_down = np.zeros(26)

    oiii_mc_err_up = np.zeros(26)
    oiii_mc_err_down = np.zeros(26)

    sii_mc_err_up = np.zeros(26)
    sii_mc_err_down = np.zeros(26)

    neiii_mc_err_up = np.zeros(26)
    neiii_mc_err_down = np.zeros(26)

    #Iterate over each galaxy

    for i in range(26):

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

        print(f"Error propagation for LzLCS galaxy {i+1}/26 complete.")

    #Ionisation parameters for ICFs
    w = OIII/(OIII + OII)
    w_err_up = np.sqrt((oiii_mc_err_up**2 * (1/(OIII + OII) - OIII/(OIII + OII)**2)**2) + (oii_mc_err_up**2 * (OIII/(OIII + OII)**2)**2))
    w_err_down = np.sqrt((oiii_mc_err_down**2 * (1/(OIII + OII) - OIII/(OIII + OII)**2)**2) + (oii_mc_err_down**2 * (OIII/(OIII + OII)**2)**2))
    
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
    mass = pd.read_excel(lzlcs_cel_filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:26]
    mass_err = pd.read_excel(lzlcs_cel_filepath, usecols = "AY", skiprows = 0).to_numpy().flatten()[0:26]
    sfr = pd.read_csv(lzlcs_sfr_filepath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()[0:26]
    sfr_err = pd.read_csv(lzlcs_sfr_filepath, delimiter = ",", usecols = [3], header = 0).to_numpy().flatten()[0:26]

    data = np.column_stack((names, mass, mass_err, sfr, sfr_err, T_e_o_iii, T_e_s_iii, T_e_o_ii, Z, Z_err_up, Z_err_down, log_Ne_O, log_Ne_O_err_up, log_Ne_O_err_down, 
                            w, w_err_up, w_err_down))

    df = pd.DataFrame(data, columns = ["galaxy", "mass", "mass_err", "sfr", 
                                    "sfr_err", "T_e_o_iii", "T_e_s_iii", 
                                    "T_e_o_ii", "Z", "Z_err_up", "Z_err_down",  
                                    "log_Ne_O", "log_Ne_O_err_up", "log_Ne_O_err_down",
                                    "ion_param", "ion_param_err_up", "ion_param_err_down"])
    
    df.to_csv("lzlcsextras.csv", index=False)

def main():
    LzLCS()

main()











