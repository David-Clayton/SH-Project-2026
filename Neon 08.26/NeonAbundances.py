import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():

    """Remake the Ne/O vs. 12+log(O/H) diagram for only the LzLCS galaxies, with datapoints 
    colour-coded to the O32 emission line ratio, which traces the ionisation parameter"""

    lzlcs_cel = r"C:\Users\drcla\OneDrive\Senior Honours Project\Neon 08.26\Final_LYC_EMISSION_LINES_David.xlsx"
    lzlcs_abundance = r"C:\Users\drcla\OneDrive\Senior Honours Project\Neon 08.26\lzlcsextras.csv"

    names = pd.read_excel(lzlcs_cel, usecols = "A", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3727 = pd.read_excel(lzlcs_cel, usecols = "J", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3729 = pd.read_excel(lzlcs_cel, usecols = "L", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_5007 = pd.read_excel(lzlcs_cel, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:27]

    ion_param = np.log10(o_iii_5007 / (o_ii_3727 + o_ii_3729)) 

    Z = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    Z_err_up = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [9], header = 0).to_numpy().flatten()
    Z_err_down = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [10], header = 0).to_numpy().flatten()

    Ne = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [11], header = 0).to_numpy().flatten()
    Ne_err_up = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [12], header = 0).to_numpy().flatten()
    Ne_err_down = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [13], header = 0).to_numpy().flatten()

    Z_err = np.stack((Z_err_up, Z_err_down), axis = 0)
    Ne_err = np.stack((Ne_err_up, Ne_err_down), axis = 0)

    plot = plt.scatter(Z, Ne, s = 20, c = ion_param, ls = "", cmap = "viridis")
    plt.errorbar(Z, Ne, xerr = Z_err, yerr = Ne_err, fmt = "none", ecolor = "gray",
                 elinewidth = 0.7, alpha = 0.6, zorder = 1)
    plt.xlabel(r"$12 + log_{10}(O/H)$", fontsize = 12)
    plt.ylabel(r"$log_{10}(Ne/O)$", fontsize = 12)

    colorbar = plt.colorbar(plot)
    colorbar.set_label(r"O32")

    plt.axhline(np.log10(0.24), color = "red", label = "Solar abundance") #(Asplund+2021)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Ne-OH.png")
    plt.show()

    #Save data
    data = np.column_stack((names, Z, Z_err_up, Z_err_down, Ne, Ne_err_up,
                            Ne_err_down, ion_param))

    df = pd.DataFrame(data, columns = ["galaxy", "Z", "Z_err_up", "Z_err_down", 
                                           "Ne", "Ne_err_up", "Ne_err_down", 
                                           "O32"])
        
    df.to_csv("Neondata060826.csv", index=False)
    
main()

