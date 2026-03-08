import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pyneb as pn

def main():

    filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\CLASSY\Final_CLASSY_EMISSION_LINES_David.xlsx"

    #Extract SII, OIII and OII emission lines with uncertainties

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    N2 = pn.Atom("N", 2)

    diags = pn.Diagnostics()

    h_beta = pd.read_excel(filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_5007 = pd.read_excel(filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959 = pd.read_excel(filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363 = pd.read_excel(filepath, usecols = "R", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3727 = pd.read_excel(filepath, usecols = "B", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729 = pd.read_excel(filepath, usecols = "F", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320 = pd.read_excel(filepath, usecols = "CB", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330 = pd.read_excel(filepath, usecols = "CF", skiprows = 0).to_numpy().flatten()[0:45]
    n_ii_6584 = pd.read_excel(filepath, usecols = "BP", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6717 = pd.read_excel(filepath, usecols = "BT", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731 = pd.read_excel(filepath, usecols = "BX", skiprows = 0).to_numpy().flatten()[0:45]

    #Errors on intensities

    h_beta_err_up = pd.read_excel(filepath, usecols = "AO", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_5007_err_up = pd.read_excel(filepath, usecols = "AW", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959_err_up = pd.read_excel(filepath, usecols = "AS", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363_err_up = pd.read_excel(filepath, usecols = "S", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3727_err_up = pd.read_excel(filepath, usecols = "C", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729_err_up = pd.read_excel(filepath, usecols = "G", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320_err_up = pd.read_excel(filepath, usecols = "CC", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330_err_up = pd.read_excel(filepath, usecols = "CG", skiprows = 0).to_numpy().flatten()[0:45]
    n_ii_6584_err_up = pd.read_excel(filepath, usecols = "BQ", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6717_err_up = pd.read_excel(filepath, usecols = "BU", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731_err_up = pd.read_excel(filepath, usecols = "BY", skiprows = 0).to_numpy().flatten()[0:45]

    h_beta_err_down = pd.read_excel(filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_5007_err_down = pd.read_excel(filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959_err_down = pd.read_excel(filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363_err_down = pd.read_excel(filepath, usecols = "T", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3727_err_down = pd.read_excel(filepath, usecols = "D", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729_err_down = pd.read_excel(filepath, usecols = "H", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320_err_down = pd.read_excel(filepath, usecols = "CD", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330_err_down = pd.read_excel(filepath, usecols = "CH", skiprows = 0).to_numpy().flatten()[0:45]
    n_ii_6584_err_down = pd.read_excel(filepath, usecols = "BR", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6717_err_down = pd.read_excel(filepath, usecols = "BV", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731_err_down = pd.read_excel(filepath, usecols = "BZ", skiprows = 0).to_numpy().flatten()[0:45]

    #Take means of errors to get single error for Monte Carlo

    o_iii_5007_err = (o_iii_5007_err_up + o_iii_5007_err_down) / 2
    o_iii_4363_err = (o_iii_4363_err_up + o_iii_4363_err_down) / 2
    o_ii_3727_err = (o_ii_3727_err_up + o_ii_3727_err_down) / 2
    o_ii_3729_err = (o_ii_3729_err_up + o_ii_3729_err_down) / 2
    o_ii_7320_err = (o_ii_7320_err_up + o_ii_7320_err_down) / 2
    o_ii_7330_err = (o_ii_7330_err_up + o_ii_7330_err_down) / 2
    s_ii_6717_err = (s_ii_6717_err_up + s_ii_6717_err_down) / 2
    s_ii_6731_err = (s_ii_6731_err_up + s_ii_6731_err_down) / 2
    h_beta_err = (h_beta_err_up + h_beta_err_down) / 2
    o_iii_4959_err = (o_iii_4959_err_down + o_iii_4959_err_up) / 2
    n_ii_6584_err = (n_ii_6584_err_up + n_ii_6584_err_down) / 2

    #Intensity ratios for temperature errors

    oiii_ratio_T = o_iii_4363/o_iii_5007
    oii_ratio_T = (o_ii_3727 + o_ii_3729) / (o_ii_7320 + o_ii_7330)
    sii_ratio_T = s_ii_6731/s_ii_6717

    #Errors on temp ratios
    oiii_err_T = oiii_ratio_T * np.sqrt((o_iii_4363_err / o_iii_4363) ** 2 + (o_iii_5007_err / o_iii_5007) ** 2)
    sii_err_T = sii_ratio_T * np.sqrt((s_ii_6717_err / s_ii_6717) ** 2 + (s_ii_6731_err / s_ii_6731) ** 2)

    #OII error is more complicated - do in steps

    first_term = (o_ii_3727_err ** 2 + o_ii_3729_err ** 2) / ((o_ii_3727 + o_ii_3729) ** 2)
    second_term = (o_ii_7320_err ** 2 + o_ii_7330_err ** 2) / ((o_ii_7320 + o_ii_7330) ** 2)
    oii_err_T = oii_ratio_T * np.sqrt(first_term + second_term)


    #Intensity ratios for abundances
    o_iii_ratio_ab = (o_iii_4959 + o_iii_5007) / h_beta
    o_ii_ratio_ab_1 = (o_ii_3727 + o_ii_3729) / h_beta #Primary
    o_ii_ratio_ab_2 = (o_ii_7320 + o_ii_7330) / h_beta #Backup if above lines not present
    n_ii_ratio_ab = n_ii_6584 / h_beta

    #Errors on abundance ratios
    o_iii_err_ab = o_iii_ratio_ab * np.sqrt(((o_iii_4959_err**2 + o_iii_5007_err**2) / (o_iii_5007 + o_iii_4959)**2) + (h_beta_err/h_beta)**2)
    o_ii_1_err_ab = o_ii_ratio_ab_1  * np.sqrt(((o_ii_3727_err**2 + o_ii_3729_err**2) / (o_ii_3729 + o_ii_3727)**2) + (h_beta_err/h_beta)**2)
    o_ii_2_err_ab = o_ii_ratio_ab_2  * np.sqrt(((o_ii_7320_err**2 + o_ii_7330_err**2) / (o_ii_7320 + o_ii_7330)**2) + (h_beta_err/h_beta)**2)
    n_ii_err_ab = n_ii_ratio_ab * np.sqrt((n_ii_6584_err/n_ii_6584)**2 + (h_beta_err/h_beta)**2)


    # Get Gaussian distributions for intensity ratios of each galaxy
    #Takes too long to do it all at once - do it iteratively for each galaxy

    oiii_T = np.zeros(len(oiii_ratio_T))
    oiii_T_err_u = np.zeros(len(oiii_T))
    oiii_T_err_d = np.zeros(len(oiii_T))

    oii_T = np.zeros(len(oii_ratio_T))
    oii_T_err_u = np.zeros(len(oii_T))
    oii_T_err_d = np.zeros(len(oii_T))


    oii_ab = np.zeros(len(o_ii_ratio_ab_1))
    oii_ab_err_u = np.zeros(len(oii_ab))
    oii_ab_err_d = np.zeros(len(oii_ab))

    oiii_ab = np.zeros(len(o_iii_ratio_ab))
    oiii_ab_err_u = np.zeros(len(oiii_ab))
    oiii_ab_err_d = np.zeros(len(oiii_ab))

    nii_ab = np.zeros(len(n_ii_ratio_ab))
    nii_ab_err_u = np.zeros(len(nii_ab))
    nii_ab_err_d = np.zeros(len(nii_ab))

    for i in range(len(oiii_T)): #All arrays are the same length - doesn't matter which I choose
        
        ####Temperature errors

        #Get intensity distributions for each galaxy
        oiii_dist = np.random.normal(oiii_ratio_T[i], oiii_err_T[i], size = 1000)
        oii_dist = np.random.normal(oii_ratio_T[i], oii_err_T[i], size = 1000)
        sii_dist = np.random.normal(sii_ratio_T[i], sii_err_T[i], size = 1000)

        #Distribution of densities and OIII region temperatures for galaxy
        [oiii_T_e_err,n_e_err] = diags.getCrossTemDen('[OIII] 4363/5007', '[SII] 6731/6716', oiii_dist, sii_dist)
        #Distributions of OII region temperatures for each galaxy
        n_e_err = np.nan_to_num(n_e_err, 100)
        oii_T_e_err = O2.getTemDen(oii_dist, den = n_e_err, to_eval = "(L(3726)+L(3729))/(L(7319)+L(7320)+L(7331)+L(7333))")

        #Expand T[OIII] sample with Garnett
        expansion = (oii_T_e_err - 3000) / 0.7
        oiii_T_e_err = np.nan_to_num(oiii_T_e_err, nan = expansion)
        #Replace T[OII] sample with Garnett
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
        o_ii_dist_1 = np.random.normal(o_ii_ratio_ab_1[i], o_ii_1_err_ab[i], size = 1000)
        o_ii_dist_2 = np.random.normal(o_ii_ratio_ab_2[i], o_ii_2_err_ab[i], size = 1000)
        n_ii_dist = np.random.normal(n_ii_ratio_ab[i], n_ii_err_ab[i], size = 1000)
        
        #Abundance distributions
        o_iii_ab = O3.getIonAbundance(o_iii_dist, tem = oiii_T_e_err, den = n_e_err, to_eval = "L(4959)+L(5007)", Hbeta = 1)
        o_ii_ab_1 = O2.getIonAbundance(o_ii_dist_1, tem = oii_T_e_err, den = n_e_err, to_eval = "L(3726)+L(3729)", Hbeta = 1)
        o_ii_ab_2 = O2.getIonAbundance(o_ii_dist_2, tem = oii_T_e_err, den = n_e_err, to_eval = "(L(7319)+L(7320)+L(7331)+L(7333))", Hbeta = 1)
        n_ii_ab = N2.getIonAbundance(n_ii_dist, tem = oii_T_e_err, den = n_e_err, to_eval = "L(6584)", Hbeta = 1)

        o_ii_ab = np.nan_to_num(o_ii_ab_1, nan = o_ii_ab_2)

        #Medians of distributions

        median_oiii_ab = np.nanmedian(o_iii_ab)
        median_oii_ab = np.nanmedian(o_ii_ab)
        median_nii_ab = np.nanmedian(n_ii_ab)

        #print(f"{median_oiii_ab}, {np.median(o_iii_ab)}")
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

        print(f"Galaxy {i+1}/45 has metallicity {12 + np.log10(oiii_ab[i] + oii_ab[i])}")
        print(f"Galaxty {i+1}/45 has log(N/O) {np.log10(nii_ab[i]/(oii_ab[i] + oiii_ab[i]))}")

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
    data = np.column_stack((metallicity_err_up, metallicity_err_down, log_n_o_err_up, log_n_o_err_down))
    np.savetxt("Abundanceswerrors.csv", data, delimiter=",", header = "12 + log(O/H) plus err, 12 + log(O/H) minus err , N/O plus err, N/O minus err")

main()
    

