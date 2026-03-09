import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyneb as pn

def fix_nan_issues(array):
    """Replace missing data in the LzLCS dataset from -999.999 to nan"""
    array[array == -999.999] = np.nan
    return array

def main():

    filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Final_LYC_EMISSION_LINES_David.xlsx"

    #Extract SII, OIII and OII emission lines with uncertainties

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    N2 = pn.Atom("N", 2)

    diags = pn.Diagnostics()

    h_beta = pd.read_excel(filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_5007 = pd.read_excel(filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959 = pd.read_excel(filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363 = pd.read_excel(filepath, usecols = "V", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3727 = pd.read_excel(filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729 = pd.read_excel(filepath, usecols = "L", skiprows = 0).to_numpy().flatten()[0:45]
    n_ii_6584 = pd.read_excel(filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6717 = pd.read_excel(filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731 = pd.read_excel(filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:45]

    #Errors on intensities
    h_beta_err = pd.read_excel(filepath, usecols = "AA", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_5007_err = pd.read_excel(filepath, usecols = "AE", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959_err = pd.read_excel(filepath, usecols = "AC", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363_err = pd.read_excel(filepath, usecols = "W", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3727_err = pd.read_excel(filepath, usecols = "K", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729_err = pd.read_excel(filepath, usecols = "M", skiprows = 0).to_numpy().flatten()[0:45]
    n_ii_6584_err = pd.read_excel(filepath, usecols = "AQ", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6717_err = pd.read_excel(filepath, usecols = "AS", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731_err = pd.read_excel(filepath, usecols = "AU", skiprows = 0).to_numpy().flatten()[0:45]
   
    #Replace placeholder data with nan
    h_beta = fix_nan_issues(h_beta)
    h_beta_err = fix_nan_issues(h_beta_err)
    o_iii_5007 = fix_nan_issues(o_iii_5007)
    o_iii_5007_err = fix_nan_issues(o_iii_5007_err)
    o_iii_4959 = fix_nan_issues(o_iii_4959)
    o_iii_4959_err = fix_nan_issues(o_iii_4959_err)
    o_iii_4363 = fix_nan_issues(o_iii_4363)
    o_iii_4363_err = fix_nan_issues(o_iii_4363_err)
    o_ii_3727 = fix_nan_issues(o_ii_3727)
    o_ii_3727_err = fix_nan_issues(o_ii_3727_err)
    o_ii_3729 = fix_nan_issues(o_ii_3729)
    o_ii_3729_err = fix_nan_issues(o_ii_3729_err)
    n_ii_6584 = fix_nan_issues(n_ii_6584)
    n_ii_6584_err = fix_nan_issues(n_ii_6584_err)
    s_ii_6717 = fix_nan_issues(s_ii_6717)
    s_ii_6717_err = fix_nan_issues(s_ii_6717_err)
    s_ii_6731 = fix_nan_issues(s_ii_6731)
    s_ii_6731_err = fix_nan_issues(s_ii_6731_err)

    #Intensity ratios for temperature errors

    oiii_ratio_T = o_iii_4363/o_iii_5007
    sii_ratio_T = s_ii_6731/s_ii_6717

    #print(sii_ratio_T)

    #No [OII]7320,30 lines, so can't directly compute temperature - need Garnett 1992

    #Errors on temp ratios
    oiii_err_T = oiii_ratio_T * np.sqrt((o_iii_4363_err / o_iii_4363) ** 2 + (o_iii_5007_err / o_iii_5007) ** 2)
    sii_err_T = sii_ratio_T * np.sqrt((s_ii_6717_err / s_ii_6717) ** 2 + (s_ii_6731_err / s_ii_6731) ** 2)

    #print(sii_err_T)

    #Intensity ratios for abundances
    o_iii_ratio_ab = (o_iii_4959 + o_iii_5007) / h_beta
    o_ii_ratio_ab = (o_ii_3727 + o_ii_3729) / h_beta #Primary
    n_ii_ratio_ab = n_ii_6584 / h_beta

    #Errors on abundance ratios
    o_iii_err_ab = o_iii_ratio_ab * np.sqrt(((o_iii_4959_err**2 + o_iii_5007_err**2) / (o_iii_5007 + o_iii_4959)**2) + (h_beta_err/h_beta)**2)
    o_ii_err_ab = o_ii_ratio_ab  * np.sqrt(((o_ii_3727_err**2 + o_ii_3729_err**2) / (o_ii_3729 + o_ii_3727)**2) + (h_beta_err/h_beta)**2)
    n_ii_err_ab = n_ii_ratio_ab * np.sqrt((n_ii_6584_err/n_ii_6584)**2 + (h_beta_err/h_beta)**2)


    # Get Gaussian distributions for intensity ratios of each galaxy
    #Takes too long to do it all at once - do it iteratively for each galaxy

    oiii_T = np.zeros(len(oiii_ratio_T))
    oiii_T_err_u = np.zeros(len(oiii_T))
    oiii_T_err_d = np.zeros(len(oiii_T))

    oii_T = np.zeros(len(oiii_ratio_T))
    oii_T_err_u = np.zeros(len(oii_T))
    oii_T_err_d = np.zeros(len(oii_T))


    oii_ab = np.zeros(len(o_ii_ratio_ab))
    oii_ab_err_u = np.zeros(len(oii_ab))
    oii_ab_err_d = np.zeros(len(oii_ab))

    oiii_ab = np.zeros(len(o_iii_ratio_ab))
    oiii_ab_err_u = np.zeros(len(oiii_ab))
    oiii_ab_err_d = np.zeros(len(oiii_ab))

    nii_ab = np.zeros(len(n_ii_ratio_ab))
    nii_ab_err_u = np.zeros(len(nii_ab))
    nii_ab_err_d = np.zeros(len(nii_ab))

    #Get intensity distributions for each galaxy
    oiii_dist = np.random.normal(oiii_ratio_T[0], oiii_err_T[0], size = 1000)
    sii_dist = np.random.normal(sii_ratio_T[0], sii_err_T[0], size = 1000)
    #print(f"{oiii_dist}, {sii_dist}")
    #Distribution of densities and OIII region temperatures for galaxy
    [oiii_T_e_err,n_e_err] = diags.getCrossTemDen('[OIII] 4363/5007', '[SII] 6731/6716', oiii_dist[0], sii_dist[0])
    #print(f"{oiii_T_e_err}, {n_e_err}")

    for i in range(len(oiii_T)): #All arrays are the same length - doesn't matter which I choose
        
        ####Temperature errors

        #Get intensity distributions for each galaxy
        oiii_dist = np.random.normal(oiii_ratio_T[i], oiii_err_T[i], size = 1000)
        sii_dist = np.random.normal(sii_ratio_T[i], sii_err_T[i], size = 1000)

        #Distribution of densities and OIII region temperatures for galaxy
        [oiii_T_e_err,n_e_err] = diags.getCrossTemDen('[OIII] 4363/5007', '[SII] 6731/6716', oiii_dist, sii_dist)
        #Distributions of OII region temperatures for each galaxy
        n_e_err = np.nan_to_num(n_e_err, 100)
        #Derive T[OII] sample with Garnett
        oii_T_e_err = 0.7 * oiii_T_e_err + 3000
        
        #Take median of distributions to get T_e and n_e
        median_T_e_oiii = np.nanmedian(oiii_T_e_err)
        median_T_e_oii = np.nanmedian(oii_T_e_err)

        #Get error on median as values one sigma away from median
        #Upper error T
        T_e_oiii_err_up = np.nanpercentile(oiii_T_e_err, 84) - median_T_e_oiii
        #Lower error T
        T_e_oiii_err_down = median_T_e_oiii - np.nanpercentile(oiii_T_e_err, 16)
        #Upper error n
        T_e_oii_err_up = np.nanpercentile(oii_T_e_err, 84) - median_T_e_oii
        #Lower error n
        T_e_oii_err_down = median_T_e_oii - np.nanpercentile(oii_T_e_err, 16)

        oiii_T[i] = median_T_e_oiii
        oiii_T_err_u[i] = T_e_oiii_err_up
        oiii_T_err_d[i] = T_e_oiii_err_down
        oii_T[i] = median_T_e_oii
        oii_T_err_u[i] = T_e_oii_err_up
        oii_T_err_d[i] = T_e_oii_err_down

        print(f"OIII T_e of galaxy {i+1} is {oiii_T[i]}K  +{oiii_T_err_u[i]}, -{oiii_T_err_d[i]}")
        print(f"OII T_e of galaxy {i+1} is {oii_T[i]}K  +{oii_T_err_u[i]}, -{oii_T_err_d[i]}")
        
        ####Abundance errors

        #Get intensity distributions for each galaxy

        o_iii_dist = np.random.normal(o_iii_ratio_ab[i], o_iii_err_ab[i], size = 1000)
        o_ii_dist = np.random.normal(o_ii_ratio_ab[i], o_ii_err_ab[i], size = 1000)
        n_ii_dist = np.random.normal(n_ii_ratio_ab[i], n_ii_err_ab[i], size = 1000)
        
        #Abundance distributions
        o_iii_ab = O3.getIonAbundance(o_iii_dist, tem = oiii_T_e_err, den = n_e_err, to_eval = "L(4959)+L(5007)", Hbeta = 1)
        o_ii_ab = O2.getIonAbundance(o_ii_dist, tem = oii_T_e_err, den = n_e_err, to_eval = "L(3726)+L(3729)", Hbeta = 1)
        n_ii_ab = N2.getIonAbundance(n_ii_dist, tem = oii_T_e_err, den = n_e_err, to_eval = "L(6584)", Hbeta = 1)

        #Medians of distributions

        median_oiii_ab = np.nanmedian(o_iii_ab)
        median_oii_ab = np.nanmedian(o_ii_ab)
        median_nii_ab = np.nanmedian(n_ii_ab)

        oiii_ab[i] = median_oiii_ab
        oii_ab[i] = median_oii_ab
        nii_ab[i] = median_nii_ab
        #Upper errors
        oiii_ab_err_up = np.nanpercentile(o_iii_ab, 84) - median_oiii_ab
        oii_ab_err_up = np.nanpercentile(o_ii_ab, 84) - median_oii_ab
        nii_ab_err_up = np.nanpercentile(n_ii_ab, 84) - median_nii_ab

        oiii_ab_err_u[i] = oiii_ab_err_up
        oii_ab_err_u[i] = oii_ab_err_up
        nii_ab_err_u[i] = nii_ab_err_up

        #Lower errors
        oiii_ab_err_down = median_oiii_ab - np.nanpercentile(o_iii_ab, 16)
        oii_ab_err_down = median_oii_ab - np.nanpercentile(o_ii_ab, 16)
        nii_ab_err_down = median_nii_ab - np.nanpercentile(n_ii_ab, 16)
        
        oiii_ab_err_d[i] = oiii_ab_err_down
        oii_ab_err_d[i] = oii_ab_err_down
        nii_ab_err_d[i] = nii_ab_err_down

        print(f"Galaxy {i+1}/27 has metallicity {12 + np.log10(oiii_ab[i] + oii_ab[i])}")
        print(f"Galaxy {i+1}/27 has log(N/O) {np.log10(nii_ab[i]/(oii_ab[i] + oiii_ab[i]))}")

    #Propagate errors
    #Oxygen
    o_ab = oiii_ab + oii_ab
    o_ab_err_up = np.sqrt(oii_ab_err_u**2 + oiii_ab_err_u**2)
    o_ab_err_down = np.sqrt(oii_ab_err_d**2 + oiii_ab_err_d**2)
    #Nitrogen
    n_ab = nii_ab
    n_ab_err_up = nii_ab_err_u
    n_ab_err_down = nii_ab_err_d
    #Metallicity
    metallicity = 12 + np.log10(o_ab)
    metallicity_err_up = o_ab_err_up / (np.log(10)*o_ab)
    metallicity_err_down = o_ab_err_down / (np.log(10)*o_ab)
    #Abundance ratio
    n_o = n_ab / o_ab
    n_o_err_up = n_o * np.sqrt((n_ab_err_up/n_ab)**2 + (o_ab_err_up/o_ab)**2)
    n_o_err_down = n_o * np.sqrt((n_ab_err_down/n_ab)**2 + (o_ab_err_down/o_ab)**2)
    log_n_o = np.log10(n_o)
    log_n_o_err_up = n_o_err_up / (np.log(10)*n_o)
    log_n_o_err_down = n_o_err_down / (np.log(10)*n_o)

    T_data = np.column_stack((oiii_T, oiii_T_err_u, oiii_T_err_d, oii_T, oii_T_err_u, oii_T_err_d))
    np.savetxt("Tempswerrors.csv" , T_data, delimiter=",", header = "T[OIII], T[OIII] plus err, T[OIII] minus err, T[OII], T[OII] plus err, T[OII] minus err")
    data = np.column_stack((metallicity, metallicity_err_up, metallicity_err_down, log_n_o, log_n_o_err_up, log_n_o_err_down))
    np.savetxt("Abundanceswerrors.csv", data, delimiter=",", header = "12 + log(O/H), 12 + log(O/H) plus err, 12 + log(O/H) minus err, log(N/O), log(N/O) plus err, log(N/O) minus err")

main() 
    

