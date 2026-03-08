import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def berg(mtot):
    sfr = 0.91 * mtot - 7.25
    return sfr

def main():

    filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\CLASSY\Abundances\classy_sample_prop.csv"

    sfr = pd.read_csv(filepath, delimiter = ",", usecols = [7], header = 0).to_numpy().flatten()
    stellar_mass = pd.read_csv(filepath, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()

    #SFR/Mass fitting fcn
    bergmass = np.linspace(6, 10, 1000)
    bergsfr = berg(bergmass)

    #Plot

    plt.scatter(stellar_mass, sfr, marker="o", color = "green")
    plt.plot(bergmass, bergsfr, color = "red", label = "logSFR = 0.91 logM* -7.25 \n (Berg 2022)")
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)")
    plt.ylabel(r"$log_{10}$ of star formation rate in galaxy ($M_{\odot} yr^{-1}$)")
    plt.title(f"SFR vs. Total Stellar Mass")
    plt.legend()
    plt.savefig("SFRvMass.png")
    plt.show()

if __name__ == "__main__":
    main()