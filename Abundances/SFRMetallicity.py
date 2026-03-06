import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def nicholls()
def main():
    filepathion = r"C:\Users\drcla\OneDrive\Senior Honours Project\Abundances\IonAbundances.csv"
    filepathmass = r"C:\Users\drcla\OneDrive\Senior Honours Project\Abundances\classy_sample_prop.csv"

    sfr = pd.read_csv(filepathmass, delimiter = ",", usecols = [7], header = 0).to_numpy().flatten()
    metallicity = pd.read_csv(filepathion, delimiter = ",", usecols = [0], header = 0).to_numpy().flatten()

    #Arrays different lengths - truncate excess nans at end of metallicity 
    metallicity = metallicity[0:len(sfr)]

    #Errors
    err_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Abundances\Abundanceswerrors.csv"
    abund_ratio_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
    abund_ratio_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [3], header = 0).to_numpy().flatten()
    abund_err = np.stack((abund_ratio_upper, abund_ratio_lower), axis = 0) #N/O

    #Plot
    plt.errorbar(sfr, metallicity, yerr = abund_err, ls = "", marker = "*", color = "green")
    plt.xlabel(r"$log_{10}$ of star formation rate in galaxy ($M_{\odot} yr^{-1}$)")
    plt.ylabel(r"12 + $log_{10}(O/H)$")
    plt.title("Relationship between SFR \n and metallicity of galaxies")
    plt.savefig("SFRvMetallicity")
    plt.show()

main()