import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

def nicholls(metallicity):
    a = -1.732
    b = 2.19

    ratio = np.log10(10 ** a + 10 ** (metallicity -12 + b))
    return ratio

def main():
    filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Final_LYC_EMISSION_LINES_David.xlsx"

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    N2 = pn.Atom("N", 2)

    diags = pn.Diagnostics()

    h_beta = pd.read_excel(filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_5007 = pd.read_excel(filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4959 = pd.read_excel(filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4363 = pd.read_excel(filepath, usecols = "V", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3727 = pd.read_excel(filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3729 = pd.read_excel(filepath, usecols = "L", skiprows = 0).to_numpy().flatten()[0:27]
    n_ii_6584 = pd.read_excel(filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:27]
    s_ii_6717 = pd.read_excel(filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:27]
    s_ii_6731 = pd.read_excel(filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:27]

    #Intensity ratios for abundances
    o_iii_ratio = (o_iii_4959 + o_iii_5007) / h_beta
    o_ii_ratio = (o_ii_3727 + o_ii_3729) / h_beta #Primary
    n_ii_ratio = n_ii_6584 / h_beta

    #Intensity ratios for physical conditions
    #Temperature
    oiii_ratio = o_iii_4363/o_iii_5007
    #Density
    sii_ratio = s_ii_6731/s_ii_6717

    """Following code reused from TempDiagnostics.py"""

    #Use getCrossTemDen to compute densities
    n_e = diags.getCrossTemDen("[OIII] 4363/5007", '[SII] 6731/6716', oiii_ratio, sii_ratio)[1]
    #If no density given, default to 100 cm^-3
    #n_e = np.nan_to_num(n_e, nan = 100)
    print(n_e)
    #Calculate temperatures of regions with OIII & OII data
    o_iii_T_e = O3.getTemDen(int_ratio = oiii_ratio, den = n_e, wave1 = 4363, wave2 = 5007)
    
    o_ii_T_e = 0.7 * o_iii_T_e + 3000


    """End of reused code"""

    #Compute abundances
    #O+ / H+
    #Primary abundance diagnostic 
    o_ii_abundance = O2.getIonAbundance(o_ii_ratio, tem = o_ii_T_e, den = n_e,  to_eval = "L(3726)+L(3729)", Hbeta = 1)
    #O++ / H+
    o_iii_abundance = O3.getIonAbundance(o_iii_ratio, tem = o_iii_T_e, den = n_e, to_eval = "L(4959)+L(5007)", Hbeta = 1)
    print(o_iii_abundance)
    #N+ / H+
    n_ii_abundance = N2.getIonAbundance(n_ii_ratio, tem = o_ii_T_e, den = n_e, to_eval = "L(6584)", Hbeta = 1)


    #Combine O+ and O++ abundances to get total O abundance
    #O/H
    o_h = (o_ii_abundance + o_iii_abundance) 
    #N/O ~ N+/O+
    n_o = n_ii_abundance / o_ii_abundance 

    #Metallicity formula
    metallicity = np.log10(o_h) + 12
    log_n_o = np.log10(n_o)

    #Errors
    err_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Abundances\Abundanceswerrors.csv"
    metallicity_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()
    metallicity_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
    abund_ratio_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [4], header = 0).to_numpy().flatten()
    abund_ratio_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [5], header = 0).to_numpy().flatten()

    #stack
    met_err = np.stack((metallicity_lower, metallicity_upper), axis = 0) #12 + log(O/H)
    ratio_err = np.stack((abund_ratio_lower, abund_ratio_upper), axis = 0) #log(N/O)

    x_nicholls = np.linspace(7.2, 9.3, 1000)
    y_nicholls = nicholls(x_nicholls)

    #Plot to compare to classy xii fig 2
    plt.errorbar(metallicity[0:27], log_n_o[0:27], yerr = ratio_err, xerr = met_err, linestyle = "", marker = "^", color = "b")
    plt.plot(x_nicholls, y_nicholls, color = "green", label = "Nicholls 2017")
    plt.xlabel("12 + log(O/H)")
    plt.ylabel("log(N/O)")
    plt.title("Metallicity")
    plt.legend()
    plt.savefig("Metallicity")
    plt.show()

    #Count how many points are in scatter plot
    print(np.sum(~np.isnan(metallicity * n_o)))

    ion_data = np.column_stack((metallicity, log_n_o))
    np.savetxt("IonAbundances.csv", ion_data, delimiter=",", header = "12 + log(O/H) , log(N/O)")

main()