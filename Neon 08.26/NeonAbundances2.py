import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm

def main():

    """Remake the Ne/O vs. 12+log(O/H) diagram for only the LzLCS galaxies, with datapoints 
    colour-coded to the O32 emission line ratio, which traces the ionisation parameter"""

    lzlcs_cel = r"C:\Users\drcla\OneDrive\Senior Honours Project\Neon 08.26\Final_LYC_EMISSION_LINES_David.xlsx"
    lzlcs_abundance = r"C:\Users\drcla\OneDrive\Senior Honours Project\Neon 08.26\amayo.csv" #Data from using Amayo ICF

    names = pd.read_excel(lzlcs_cel, usecols = "A", skiprows = 0).to_numpy().flatten()[0:26]
    o_ii_3727 = pd.read_excel(lzlcs_cel, usecols = "J", skiprows = 0).to_numpy().flatten()[0:26]
    o_ii_3729 = pd.read_excel(lzlcs_cel, usecols = "L", skiprows = 0).to_numpy().flatten()[0:26]
    o_iii_5007 = pd.read_excel(lzlcs_cel, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:26]

    o_ii_3727_err = pd.read_excel(lzlcs_cel, usecols = "K", skiprows = 0).to_numpy().flatten()[0:26]
    o_ii_3729_err = pd.read_excel(lzlcs_cel, usecols = "M", skiprows = 0).to_numpy().flatten()[0:26]
    o_iii_5007_err = pd.read_excel(lzlcs_cel, usecols = "AE", skiprows = 0).to_numpy().flatten()[0:26]

    O32 = np.log10(o_iii_5007 / (o_ii_3727 + o_ii_3729)) 
    O32_err = np.sqrt(((o_iii_5007_err/o_iii_5007)**2 + (o_ii_3727_err**2 + o_ii_3729_err**2)/(o_ii_3727+o_ii_3729)**2))/np.log(10)

    Z = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    Z_err_up = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [9], header = 0).to_numpy().flatten()
    Z_err_down = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [10], header = 0).to_numpy().flatten()

    Ne = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [11], header = 0).to_numpy().flatten()
    Ne_err_up = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [12], header = 0).to_numpy().flatten()
    Ne_err_down = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [13], header = 0).to_numpy().flatten()

    ion_param = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [14], header = 0).to_numpy().flatten()
    ion_param_err_up = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [15], header = 0).to_numpy().flatten()
    ion_param_err_down = pd.read_csv(lzlcs_abundance, delimiter = ",", usecols = [16], header = 0).to_numpy().flatten()
    
    Z_err = np.stack((Z_err_up, Z_err_down), axis = 0)
    Ne_err = np.stack((Ne_err_up, Ne_err_down), axis = 0)
    ion_param_err = np.stack((ion_param_err_up, ion_param_err_down), axis = 0)


    plot = plt.scatter(Z, Ne, s = 20, c = O32, ls = "", cmap = "viridis")
    plt.errorbar(Z, Ne, xerr = Z_err, yerr = Ne_err, fmt = "none", ecolor = "gray",
                 elinewidth = 0.7, alpha = 0.6, zorder = 1)
    plt.xlabel(r"$12 + log_{10}(O/H)$", fontsize = 12)
    plt.ylabel(r"$log_{10}(Ne/O)$", fontsize = 12)
    plt.title(r"Amayo ICF")

    colorbar = plt.colorbar(plot)
    colorbar.set_label(r"O32")

    plt.axhline(np.log10(0.24), color = "red", label = "Solar abundance \n (Asplund+2021)") #(Asplund+2021)
    plt.axvline(8.2, color = "orange", label = "Isotov+2006 boundary")
    plt.legend()
    plt.tight_layout()
    plt.savefig("Ne-OH_Amayo.png")
    plt.show()

    plot = plt.scatter(O32, Ne, s = 20, c = Z, ls = "", cmap = "viridis")
    plt.errorbar(O32, Ne, xerr = O32_err, yerr = Ne_err, fmt = "none", ecolor = "gray",
                elinewidth = 0.7, alpha = 0.6, zorder = 1)
    plt.xlabel(r"O32", fontsize = 12)
    plt.ylabel(r"$log_{10}(Ne/O)$", fontsize = 12)
    plt.title(r"Amayo ICF")
    
    colorbar = plt.colorbar(plot)
    colorbar.set_label(r"$12 + log_{10}(O/H)$")
    
    plt.axhline(np.log10(0.24), color = "red", label = "Solar abundance \n (Asplund+2021)") #(Asplund+2021)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Ne-O32_Amayo.png")
    plt.show()

    #Split data into three bins based on metallicity
    #To check for consequences of metallicity dependence of Isotov+2006 ICFs

    plot = plt.scatter(ion_param[Z<7.2], Ne[Z<7.2], s = 20, c = "red", ls = "", label = "Z<7.2")
    plot = plt.scatter(ion_param[(Z>7.2) & (Z<8.2)], Ne[(Z>7.2) & (Z<8.2)], s = 20, c = "green", ls = "", label = "7.2<Z<8.2")
    plot = plt.scatter(ion_param[Z>8.2], Ne[Z>8.2], s = 20, c = "blue", ls = "", label = "Z>8.2")
    plt.errorbar(ion_param, Ne, xerr = ion_param_err, yerr = Ne_err, fmt = "none", ecolor = "gray",
                 elinewidth = 0.7, alpha = 0.6, zorder = 1)
    plt.xlabel(r"$O^{++}/(O^+ + O^{++})$", fontsize = 12)
    plt.ylabel(r"$log_{10}(Ne/O)$", fontsize = 12)
    plt.title(r"Amayo ICF")
    
    plt.axhline(np.log10(0.24), color = "red", label = "Solar abundance \n (Asplund+2021)") #(Asplund+2021)
    plt.xlim(0, 1)
    plt.ylim(-1.0, -0.2)
    plt.legend()
    plt.tight_layout()
    plt.savefig("Ne-ip_Amayo.png")
    plt.show()

    #Save data
    data = np.column_stack((names, Z, Z_err_up, Z_err_down, Ne, Ne_err_up,
                            Ne_err_down, O32, O32_err, ion_param, ion_param_err_up,
                            ion_param_err_down))

    df = pd.DataFrame(data, columns = ["galaxy", "Z", "Z_err_up", "Z_err_down", 
                                           "Ne", "Ne_err_up", "Ne_err_down", 
                                           "O32", "O32_err", "ion_param", "ion_param_err_up",
                                           "ion_param_err_down"])
        
    df.to_csv("Neondata150826.csv", index=False)

main()

