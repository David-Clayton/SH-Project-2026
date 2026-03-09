import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    filepathion = r"C:\Users\drcla\OneDrive\Senior Honours Project\CLASSY\Abundances\IonAbundances.csv"
    filepathmass = r"C:\Users\drcla\OneDrive\Senior Honours Project\CLASSY\Abundances\classy_sample_prop.csv"

    stellar_mass = pd.read_csv(filepathmass, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()
    metallicity = pd.read_csv(filepathion, delimiter = ",", usecols = [0], header = 0).to_numpy().flatten()
    n_o = pd.read_csv(filepathion, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()

    #Arrays different lengths - truncate excess nans at end of metallicity 
    metallicity = metallicity[0:len(stellar_mass)]
    n_o = n_o[0:len(stellar_mass)]

    #Errors
    err_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\CLASSY\Abundances\Abundanceswerrors.csv"
    metal_ratio_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [0], header = 0).to_numpy().flatten()
    metal_ratio_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()
    abund_ratio_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
    abund_ratio_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [3], header = 0).to_numpy().flatten()
    metal_err = np.stack((metal_ratio_lower, metal_ratio_upper)) #12 + log(O/H)
    abund_err = np.stack((abund_ratio_lower, abund_ratio_upper), axis = 0) #log(N/O)

    #Plot
    plt.errorbar(stellar_mass, metallicity, yerr = metal_err, ls = "", marker = "s", color = "red")
    plt.axline(xy1 = (0, 6.4), slope = 0.2, color = "green", label = "12+log(O/H) = 0.2M*+6.4 \n Berg 2022")
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)")
    plt.ylabel(r"12 + $log_{10}(O/H)$")
    plt.xlim(5, 11)
    plt.legend()
    plt.title("Relationship between total stellar mass \n and metallicity of galaxies")
    plt.savefig("MassvMetallicity")
    plt.show()

    plt.errorbar(stellar_mass, n_o, yerr = abund_err, ls = "", marker = "s", color = "red")
    #plt.axline(xy1 = (0, 6.4), slope = 0.2, color = "green", label = "12+log(O/H) = 0.2M*+6.4 \n Berg 2022")
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)")
    plt.ylabel(r"$log_{10}(N/O)$")
    plt.xlim(5, 11)
    plt.ylim(-2.2, -0.5)
    #plt.legend()
    plt.title("Relationship between total stellar mass \n and N/O of galaxies")
    plt.savefig("MassvNO")
    plt.show()

main()