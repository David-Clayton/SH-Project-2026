import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    filepathion = r"C:\Users\drcla\OneDrive\Senior Honours Project\CLASSY\Abundances\IonAbundances.csv"
    filepathmass = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Final_LYC_EMISSION_LINES_David.xlsx"

    stellar_mass = pd.read_excel(filepathmass, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:27]
    metallicity = pd.read_csv(filepathion, delimiter = ",", usecols = [0], header = 0).to_numpy().flatten()
    n_o = pd.read_csv(filepathion, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()

    #Arrays different lengths - truncate excess nans at end of metallicity 
    metallicity = metallicity[0:len(stellar_mass)]
    n_o = n_o[0:len(stellar_mass)]

    #Errors
    err_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Abundances\Abundanceswerrors.csv"
    metal_ratio_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()
    metal_ratio_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
    abund_ratio_upper = pd.read_csv(err_filepath, delimiter = ",", usecols = [4], header = 0).to_numpy().flatten()
    abund_ratio_lower = pd.read_csv(err_filepath, delimiter = ",", usecols = [5], header = 0).to_numpy().flatten()
    metal_err = np.stack((metal_ratio_lower, metal_ratio_upper)) #12 + log(O/H)
    abund_err = np.stack((abund_ratio_lower, abund_ratio_upper), axis = 0) #log(N/O)
    mass_err = pd.read_excel(filepathmass, usecols = "AY", skiprows = 0).to_numpy().flatten()[0:27]

    #Plot
    plt.errorbar(stellar_mass, metallicity, yerr = metal_err, xerr = mass_err, ls = "", marker = "s", color = "red")
    plt.axline(xy1 = (0, 6.4), slope = 0.2, color = "green", label = "12+log(O/H) = 0.2M*+6.4 \n Berg 2022")
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)")
    plt.ylabel(r"12 + $log_{10}(O/H)$")
    plt.xlim(5, 11)
    plt.legend()
    plt.title("Relationship between total stellar mass \n and metallicity of galaxies")
    plt.savefig("MassvMetallicity")
    plt.show()

    plt.errorbar(stellar_mass, n_o, yerr = abund_err, xerr = mass_err, ls = "", marker = "s", color = "red")
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