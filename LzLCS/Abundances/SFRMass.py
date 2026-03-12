import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def berg(mtot):
    sfr = 0.91 * mtot - 7.25
    return sfr

def main():

    filepathmass = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Final_LYC_EMISSION_LINES_David.xlsx"
    filepathsfr = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\SFR.csv"

    sfr = pd.read_csv(filepathsfr, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
    sfr_error = pd.read_csv(filepathsfr, delimiter = ",", usecols = [3], header = 0).to_numpy().flatten()
    stellar_mass = pd.read_excel(filepathmass, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:27]
    stellar_mass_error = pd.read_excel(filepathmass, usecols = "AY", skiprows = 0).to_numpy().flatten()[0:27]

    #SFR/Mass fitting fcn
    bergmass = np.linspace(6, 10, 1000)
    bergsfr = berg(bergmass)

    #Plot

    plt.errorbar(stellar_mass, sfr, ls = "", xerr = stellar_mass_error, yerr = sfr_error, marker="o", color = "green")
    plt.plot(bergmass, bergsfr, color = "red", label = "logSFR = 0.91 logM* -7.25 \n (Berg 2022)")
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)")
    plt.ylabel(r"$log_{10}$ of star formation rate in galaxy ($M_{\odot} yr^{-1}$)")
    plt.title(f"SFR vs. Total Stellar Mass")
    plt.legend()
    plt.savefig("SFRvMass.png")
    plt.show()

if __name__ == "__main__":
    main()