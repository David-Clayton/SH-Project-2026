import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt

def metallicity(a_0, a_1, a_2, a_3, x):
    """Derive the metallicity from the polynomial parameterisation of strong line intensity ratios (x)
    given by Eq. 2 in Rosales-Ortega et al. (2026) for the case of HII regions having imhomogeneous
    temperature structures (t^2 > 0)"""

    Z = a_0 + (a_1 * x) + (a_2 * x**2) + (a_3 * x**3)

    return Z

def error(e_0, e_1, e_2, x):
    """Derive the polynomial parameterisation of the dispersion (sigma) from the strong line 
    ratios, where the error on the metallicity is given as 1*sigma"""

    sigma = e_0 + (e_1 * x) + (e_2 * x**2)

    return abs(sigma)

def fix_nan_issues(array):
    """Replace missing data in the LzLCS dataset from -999.999 to nan"""
    array[array == -999.999] = np.nan
    return array

def CLASSY():
    #CLASSY emission lines

    classy_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\Final_CLASSY_EMISSION_LINES_David.xlsx"
    classy_data_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\classyextras.csv"

    names = pd.read_excel(classy_cel_filepath, usecols = "A", skiprows = 0).to_numpy().flatten()[0:45]

    h_alpha = pd.read_excel(classy_cel_filepath, usecols = "BL", skiprows = 0).to_numpy().flatten()[0:45]
    h_beta = pd.read_excel(classy_cel_filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()[0:45]
    h_gamma = pd.read_excel(classy_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:45]

    o_ii_3727 = pd.read_excel(classy_cel_filepath, usecols = "B", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_3729 = pd.read_excel(classy_cel_filepath, usecols = "F", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7320 = pd.read_excel(classy_cel_filepath, usecols = "CB", skiprows = 0).to_numpy().flatten()[0:45]
    o_ii_7330 = pd.read_excel(classy_cel_filepath, usecols = "CF", skiprows = 0).to_numpy().flatten()[0:45]

    o_iii_5007 = pd.read_excel(classy_cel_filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4959 = pd.read_excel(classy_cel_filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:45]
    o_iii_4363 = pd.read_excel(classy_cel_filepath, usecols = "R", skiprows = 0).to_numpy().flatten()[0:45]

    n_ii_6584 = pd.read_excel(classy_cel_filepath, usecols = "BP", skiprows = 0).to_numpy().flatten()[0:45]

    s_ii_6717 = pd.read_excel(classy_cel_filepath, usecols = "BT", skiprows = 0).to_numpy().flatten()[0:45]
    s_ii_6731 = pd.read_excel(classy_cel_filepath, usecols = "BX", skiprows = 0).to_numpy().flatten()[0:45]

    s_iii_6312 = pd.read_excel(classy_cel_filepath, usecols = "BH", skiprows = 0).to_numpy().flatten()[0:45]
    s_iii_9069 = pd.read_excel(classy_cel_filepath, usecols = "CN", skiprows = 0).to_numpy().flatten()[0:45]

    ar_iii_7135 = pd.read_excel(classy_cel_filepath, usecols = "CJ", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869 = pd.read_excel(classy_cel_filepath, usecols = "CR", skiprows = 0).to_numpy().flatten()[0:45]

    fe_iii_4658 = pd.read_excel(classy_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:45]

    #Direct method metallicity
    direct_Z = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()
    direct_Z_err_up = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [7], header = 0).to_numpy().flatten()
    direct_Z_err_down = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    direct_Z_err = (direct_Z_err_up + direct_Z_err_down) / 2

    #Strong line metallicities
    #R2 method
    R2 = np.log10(o_ii_3727 / h_beta)
    Z_R2 = metallicity(8.00, 0.92, 0.40, 0.17, R2) #For t^2 > 0 (inhomogeneous case)
    sigma_R2 = error(-0.20, -0.05, 0.36, R2)

    #O32 method
    O32 = np.log10(o_iii_5007 / o_ii_3727)
    Z_O32 = metallicity(8.33, -0.32, 0.08, -0.09, O32)
    sigma_O32 = error(-0.02, 0.02, 0.30, O32)

    #Ne3O2 method
    Ne3O2 = np.log10(ne_iii_3869 / o_ii_3727)
    Z_Ne3O2 = metallicity(7.85, -0.71, -0.26, -0.05, Ne3O2)
    sigma_Ne3O2 = error(-0.02, -0.04, 0.26, Ne3O2)

    #R2Ne3 method
    R2Ne3 = np.log10((o_ii_3727 + ne_iii_3869) / h_beta)
    Z_R2Ne3 = metallicity(7.83, 1.43, 0.00, 0.00, R2Ne3)
    sigma_R2Ne3 = error(-0.57, 0.15, 0.31, R2Ne3)

    #N2 method
    N2 = np.log10(n_ii_6584 / h_alpha)
    Z_N2 = metallicity(9.27, 1.48, 0.86, 0.23, N2)
    sigma_N2 = error(0.06, 0.17, 0.33, N2)

    return (direct_Z, direct_Z_err, Z_R2, sigma_R2, Z_O32, sigma_O32, Z_Ne3O2, 
            sigma_Ne3O2, Z_R2Ne3, sigma_R2Ne3, Z_N2, sigma_N2, names)


def LzLCS():
    #LzLCS emission lines

    lzlcs_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\Final_LYC_EMISSION_LINES_David.xlsx"
    lzlcs_data_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\lzlcsextras.csv"

    names = pd.read_excel(lzlcs_cel_filepath, usecols = "A", skiprows = 0).to_numpy().flatten()[0:27]

    h_alpha = pd.read_excel(lzlcs_cel_filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()[0:27]
    h_beta = pd.read_excel(lzlcs_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:27]
    h_gamma = pd.read_excel(lzlcs_cel_filepath, usecols = "T", skiprows = 0).to_numpy().flatten()[0:27]

    o_ii_3727 = pd.read_excel(lzlcs_cel_filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:27]
    o_ii_3729 = pd.read_excel(lzlcs_cel_filepath, usecols = "L", skiprows = 0).to_numpy().flatten()[0:27]

    o_iii_5007 = pd.read_excel(lzlcs_cel_filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4959 = pd.read_excel(lzlcs_cel_filepath, usecols = "AB", skiprows = 0).to_numpy().flatten()[0:27]
    o_iii_4363 = pd.read_excel(lzlcs_cel_filepath, usecols = "V", skiprows = 0).to_numpy().flatten()[0:27]

    n_ii_6584 = pd.read_excel(lzlcs_cel_filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:45]

    s_ii_6717 = pd.read_excel(lzlcs_cel_filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()[0:27]
    s_ii_6731 = pd.read_excel(lzlcs_cel_filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()[0:27]

    ne_iii_3869 = pd.read_excel(lzlcs_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:27]

    h_alpha = fix_nan_issues(h_alpha)
    h_beta = fix_nan_issues(h_beta)
    h_gamma = fix_nan_issues(h_gamma)
    o_ii_3727 = fix_nan_issues(o_ii_3727)
    o_ii_3729 = fix_nan_issues(o_ii_3729)
    o_iii_5007 = fix_nan_issues(o_iii_5007)
    o_iii_4959 = fix_nan_issues(o_iii_4959)
    o_iii_4363 = fix_nan_issues(o_iii_4363)
    n_ii_6584 = fix_nan_issues(n_ii_6584)
    s_ii_6717 = fix_nan_issues(s_ii_6717)
    s_ii_6731 = fix_nan_issues(s_ii_6731)
    ne_iii_3869 = fix_nan_issues(ne_iii_3869)

    #Direct method metallicity
    direct_Z = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    direct_Z_err_up = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [9], header = 0).to_numpy().flatten()
    direct_Z_err_down = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [10], header = 0).to_numpy().flatten()
    direct_Z_err = (direct_Z_err_up + direct_Z_err_down) / 2

     #Strong line metallicities
    #R2 method
    R2 = np.log10(o_ii_3727 / h_beta)
    Z_R2 = metallicity(8.00, 0.92, 0.40, 0.17, R2) #For t^2 > 0 (inhomogeneous case)
    sigma_R2 = error(-0.20, -0.05, 0.36, R2)

    #O32 method
    O32 = np.log10(o_iii_5007 / o_ii_3727)
    Z_O32 = metallicity(8.33, -0.32, 0.08, -0.09, O32)
    sigma_O32 = error(-0.02, 0.02, 0.30, O32)

    #Ne3O2 method
    Ne3O2 = np.log10(ne_iii_3869 / o_ii_3727)
    Z_Ne3O2 = metallicity(7.85, -0.71, -0.26, -0.05, Ne3O2)
    sigma_Ne3O2 = error(-0.02, -0.04, 0.26, Ne3O2)

    #R2Ne3 method
    R2Ne3 = np.log10((o_ii_3727 + ne_iii_3869) / h_beta)
    Z_R2Ne3 = metallicity(7.83, 1.43, 0.00, 0.00, R2Ne3)
    sigma_R2Ne3 = error(-0.57, 0.15, 0.31, R2Ne3)

    #N2 method
    N2 = np.log10(n_ii_6584 / h_alpha)
    Z_N2 = metallicity(9.27, 1.48, 0.86, 0.23, N2)
    sigma_N2 = error(0.06, 0.17, 0.33, N2)

    return (direct_Z, direct_Z_err, Z_R2, sigma_R2, Z_O32, sigma_O32, Z_Ne3O2, 
            sigma_Ne3O2, Z_R2Ne3, sigma_R2Ne3, Z_N2, sigma_N2, names)


def main():
    (Z_dir_C, Z_dir_err_C, Z_R2_C, Z_R2_err_C, Z_O32_C, Z_O32_err_C, Z_Ne3O2_C, 
            Z_Ne3O2_err_C, Z_R2Ne3_C, Z_R2Ne3_err_C, Z_N2_C, Z_N2_err_C, names_C) = CLASSY()
    
    (Z_dir_L, Z_dir_err_L, Z_R2_L, Z_R2_err_L, Z_O32_L, Z_O32_err_L, Z_Ne3O2_L, 
            Z_Ne3O2_err_L, Z_R2Ne3_L, Z_R2Ne3_err_L, Z_N2_L, Z_N2_err_L, names_L) = LzLCS()

    plt.scatter(Z_R2_C, Z_dir_C, s = 20, ls = "", color = "slateblue", label = "CLASSY")
    plt.errorbar(Z_R2_C, Z_dir_C, xerr = Z_R2_err_C, yerr = Z_dir_err_C, fmt = "none", ecolor = "slateblue")
    plt.scatter(Z_R2_L, Z_dir_L, s = 20, ls = "", color = "salmon", label = "LzLCS")
    plt.errorbar(Z_R2_L, Z_dir_L, xerr = Z_R2_err_L, yerr = Z_dir_err_L, fmt = "none", ecolor = "salmon")
    plt.axline((8,8), slope = 1, color = "black")
    plt.xlabel(r"Z(R2 | $log_{10}$([OII]$\lambda$3727/H$\beta$))")
    plt.ylabel(r"Direct method metallicity")
    plt.tight_layout()
    plt.legend()
    plt.savefig("R2.png")
    plt.show()

    plt.scatter(Z_O32_C, Z_dir_C, s = 20, ls = "", color = "slateblue", label = "CLASSY")
    plt.errorbar(Z_O32_C, Z_dir_C, xerr = Z_O32_err_C, yerr = Z_dir_err_C, fmt = "none", ecolor = "slateblue")
    plt.scatter(Z_O32_L, Z_dir_L, s = 20, ls = "", color = "salmon", label = "LzLCS")
    plt.errorbar(Z_O32_L, Z_dir_L, xerr = Z_O32_err_L, yerr = Z_dir_err_L, fmt = "none", ecolor = "salmon")
    plt.axline((8,8), slope = 1, color = "black")
    plt.xlabel(r"Z(O32 | $log_{10}$([OIII]$\lambda$5007/[OII]$\lambda$3727))")
    plt.ylabel(r"Direct method metallicity")
    plt.tight_layout()
    plt.legend()
    plt.savefig("O32.png")
    plt.show()

    plt.scatter(Z_Ne3O2_C, Z_dir_C, s = 20, ls = "", color = "slateblue", label = "CLASSY")
    plt.errorbar(Z_Ne3O2_C, Z_dir_C, xerr = Z_Ne3O2_err_C, yerr = Z_dir_err_C, fmt = "none", ecolor = "slateblue")
    plt.scatter(Z_Ne3O2_L, Z_dir_L, s = 20, ls = "", color = "salmon", label = "LzLCS")
    plt.errorbar(Z_Ne3O2_L, Z_dir_L, xerr = Z_Ne3O2_err_L, yerr = Z_dir_err_L, fmt = "none", ecolor = "salmon")
    plt.axline((8,8), slope = 1, color = "black")
    plt.xlabel(r"Z(Ne3O2 | $log_{10}$([NeIII]$\lambda$3869/[OII]$\lambda$3727))")
    plt.ylabel(r"Direct method metallicity")
    plt.tight_layout()
    plt.legend()
    plt.savefig("Ne3O2.png")
    plt.show()

    plt.scatter(Z_R2Ne3_C, Z_dir_C, s = 20, ls = "", color = "slateblue", label = "CLASSY")
    plt.errorbar(Z_R2Ne3_C, Z_dir_C, xerr = Z_R2Ne3_err_C, yerr = Z_dir_err_C, fmt = "none", ecolor = "slateblue")
    plt.scatter(Z_R2Ne3_L, Z_dir_L, s = 20, ls = "", color = "salmon", label = "LzLCS")
    plt.errorbar(Z_R2Ne3_L, Z_dir_L, xerr = Z_R2Ne3_err_L, yerr = Z_dir_err_L, fmt = "none", ecolor = "salmon")
    plt.axline((8,8), slope = 1, color = "black")
    plt.xlabel(r"Z(O32 | $log_{10}$(([NeIII]$\lambda$3869+[OII]$\lambda$3727)/H$\beta$))")
    plt.ylabel(r"Direct method metallicity")
    plt.tight_layout()
    plt.legend()
    plt.savefig("R2Ne3.png")
    plt.show()

    plt.scatter(Z_N2_C, Z_dir_C, s = 20, ls = "", color = "slateblue", label = "CLASSY")
    plt.errorbar(Z_N2_C, Z_dir_C, xerr = Z_N2_err_C, yerr = Z_dir_err_C, fmt = "none", ecolor = "slateblue")
    plt.scatter(Z_N2_L, Z_dir_L, s = 20, ls = "", color = "salmon", label = "LzLCS")
    plt.errorbar(Z_N2_L, Z_dir_L, xerr = Z_N2_err_L, yerr = Z_dir_err_L, fmt = "none", ecolor = "salmon")
    plt.axline((8,8), slope = 1, color = "black")
    plt.xlabel(r"Z(N2 | $log_{10}$([NII]$\lambda$6584/H$\alpha$))")
    plt.ylabel(r"Direct method metallicity")
    plt.tight_layout()
    plt.legend()
    plt.savefig("N2.png")
    plt.show()

    names = np.concatenate((names_C, names_L))
    Z_dir = np.concatenate((Z_dir_C, Z_dir_L))
    Z_dir_err = np.concatenate((Z_dir_err_C, Z_dir_err_L))
    Z_R2 = np.concatenate((Z_R2_C, Z_R2_L))
    Z_R2_err = np.concatenate((Z_R2_err_C, Z_R2_err_L))
    Z_O32 = np.concatenate((Z_O32_C, Z_O32_L))
    Z_O32_err = np.concatenate((Z_O32_err_C, Z_O32_err_L))
    Z_Ne3O2 = np.concatenate((Z_Ne3O2_C, Z_Ne3O2_L))
    Z_Ne3O2_err = np.concatenate((Z_Ne3O2_err_C, Z_Ne3O2_err_L))
    Z_R2Ne3 = np.concatenate((Z_R2Ne3_C, Z_R2Ne3_L))
    Z_R2Ne3_err = np.concatenate((Z_R2Ne3_err_C, Z_R2Ne3_err_L))
    Z_N2 = np.concatenate((Z_N2_C, Z_N2_L))
    Z_N2_err = np.concatenate((Z_N2_err_C, Z_N2_err_L))

    data = np.column_stack((names, Z_dir, Z_dir_err, 
                            Z_R2, Z_R2_err, Z_O32, Z_O32_err, Z_Ne3O2, Z_Ne3O2_err, 
                            Z_R2Ne3, Z_R2Ne3_err, Z_N2, Z_N2_err))

    df = pd.DataFrame(data, columns = ["galaxy", "Z_dir", "Z_dir_err", "Z_R2", 
                                       "Z_R2_err", "Z_O32", "Z_O32_err", "Z_Ne3O2", 
                                       "Z_Ne3O2_err", "Z_R2Ne3", "Z_R2Ne3_err", "Z_N2", "Z_N2_err"])
    
    df.to_csv("Stronglinedata.csv", index=False)



main()