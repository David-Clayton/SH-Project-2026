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
    ####DISUSED

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

    o_ii_3727 = pd.read_excel(classy_cel_filepath, usecols = "B", skiprows = 0).to_numpy().flatten()[0:45]
    
    o_iii_5007 = pd.read_excel(classy_cel_filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()[0:45]

    n_ii_6584 = pd.read_excel(classy_cel_filepath, usecols = "BP", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869 = pd.read_excel(classy_cel_filepath, usecols = "CR", skiprows = 0).to_numpy().flatten()[0:45]


    h_alpha_err_u = pd.read_excel(classy_cel_filepath, usecols = "BM", skiprows = 0).to_numpy().flatten()[0:45]
    h_beta_err_u = pd.read_excel(classy_cel_filepath, usecols = "AO", skiprows = 0).to_numpy().flatten()[0:45]

    o_ii_3727_err_u = pd.read_excel(classy_cel_filepath, usecols = "C", skiprows = 0).to_numpy().flatten()[0:45]
    
    o_iii_5007_err_u = pd.read_excel(classy_cel_filepath, usecols = "AW", skiprows = 0).to_numpy().flatten()[0:45]

    n_ii_6584_err_u = pd.read_excel(classy_cel_filepath, usecols = "BQ", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869_err_u = pd.read_excel(classy_cel_filepath, usecols = "CS", skiprows = 0).to_numpy().flatten()[0:45]


    h_alpha_err_d = pd.read_excel(classy_cel_filepath, usecols = "BN", skiprows = 0).to_numpy().flatten()[0:45]
    h_beta_err_d = pd.read_excel(classy_cel_filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:45]

    o_ii_3727_err_d = pd.read_excel(classy_cel_filepath, usecols = "D", skiprows = 0).to_numpy().flatten()[0:45]
    
    o_iii_5007_err_d = pd.read_excel(classy_cel_filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()[0:45]

    n_ii_6584_err_d = pd.read_excel(classy_cel_filepath, usecols = "BR", skiprows = 0).to_numpy().flatten()[0:45]

    ne_iii_3869_err_d = pd.read_excel(classy_cel_filepath, usecols = "CT", skiprows = 0).to_numpy().flatten()[0:45]


    h_alpha_err = (h_alpha_err_u + h_alpha_err_d) / 2
    h_beta_err = (h_beta_err_u + h_beta_err_d) / 2

    o_ii_3727_err = (o_ii_3727_err_u + o_ii_3727_err_d) / 2
    
    o_iii_5007_err = (o_iii_5007_err_u + o_iii_5007_err_d) / 2
    n_ii_6584_err = (n_ii_6584_err_u + n_ii_6584_err_d) / 2

    ne_iii_3869_err = (ne_iii_3869_err_u + ne_iii_3869_err_d) / 2

    #Extend strong-line intensities to an array of intensities with the mean at the empirical value
    #And the standard deviation as the error on the empirical value

    h_alpha = np.random.normal(h_alpha[:, None], h_alpha_err[:, None], size = (45, 1000))
    h_beta = np.random.normal(h_beta[:, None], h_beta_err[:, None], size = (45, 1000))
    o_ii_3727 = np.random.normal(o_ii_3727[:, None], o_ii_3727_err[:, None], size = (45, 1000))
    o_iii_5007 = np.random.normal(o_iii_5007[:, None], o_iii_5007_err[:, None], size = (45, 1000))
    n_ii_6584 = np.random.normal(n_ii_6584[:, None], n_ii_6584_err[:, None], size = (45, 1000))
    ne_iii_3869 = np.random.normal(ne_iii_3869[:, None], ne_iii_3869_err[:, None], size = (45, 1000))

    #Direct method metallicity
    direct_Z = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()
    direct_Z_err_up = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [7], header = 0).to_numpy().flatten()
    direct_Z_err_down = pd.read_csv(classy_data_filepath, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    direct_Z_err = (direct_Z_err_up + direct_Z_err_down) / 2

    #Strong line metallicities
    #R2 method
    R2 = np.log10(o_ii_3727 / h_beta)
    Z_R2_dist = metallicity(8.00, 0.92, 0.40, 0.17, R2)  # For t^2 > 0 (inhomogeneous case)
    Z_R2_median = np.nanmedian(Z_R2_dist, axis = 1)
    Z_R2_error_up = np.nanpercentile(Z_R2_dist, 84, axis = 1) - Z_R2_median
    Z_R2_error_down = Z_R2_median - np.nanpercentile(Z_R2_dist, 16, axis = 1)

    #O32 method
    O32 = np.log10(o_iii_5007 / o_ii_3727)
    Z_O32_dist = metallicity(8.33, -0.32, 0.08, -0.09, O32)
    Z_O32_median = np.nanmedian(Z_O32_dist, axis = 1)
    Z_O32_error_up = np.nanpercentile(Z_O32_dist, 84, axis = 1) - Z_O32_median
    Z_O32_error_down = Z_O32_median - np.nanpercentile(Z_O32_dist, 16, axis = 1)

    #Ne3O2 method
    Ne3O2 = np.log10(ne_iii_3869 / o_ii_3727)
    Z_Ne3O2_dist = metallicity(7.85, -0.71, -0.26, -0.05, Ne3O2)
    Z_Ne3O2_median = np.nanmedian(Z_Ne3O2_dist, axis = 1)
    Z_Ne3O2_error_up = np.nanpercentile(Z_Ne3O2_dist, 84, axis = 1) - Z_Ne3O2_median
    Z_Ne3O2_error_down = Z_Ne3O2_median - np.nanpercentile(Z_Ne3O2_dist, 16, axis = 1)

    #R2Ne3 method
    R2Ne3 = np.log10((o_ii_3727 + ne_iii_3869) / h_beta)
    Z_R2Ne3_dist = metallicity(7.83, 1.43, 0.00, 0.00, R2Ne3)
    Z_R2Ne3_median = np.nanmedian(Z_R2Ne3_dist, axis = 1)
    Z_R2Ne3_error_up = np.nanpercentile(Z_R2Ne3_dist, 84, axis = 1) - Z_R2Ne3_median
    Z_R2Ne3_error_down = Z_R2Ne3_median - np.nanpercentile(Z_R2Ne3_dist, 16, axis = 1)

    #N2 method
    N2 = np.log10(n_ii_6584 / h_alpha)
    Z_N2_dist = metallicity(9.27, 1.48, 0.86, 0.23, N2)
    Z_N2_median = np.nanmedian(Z_N2_dist, axis = 1)
    Z_N2_error_up = np.nanpercentile(Z_N2_dist, 84, axis = 1) - Z_N2_median
    Z_N2_error_down = Z_N2_median - np.nanpercentile(Z_N2_dist, 16, axis = 1)

    return (direct_Z, direct_Z_err, Z_R2_median, (Z_R2_error_up + Z_R2_error_down)/2, Z_O32_median, (Z_O32_error_up + Z_O32_error_down)/2, Z_Ne3O2_median, (Z_Ne3O2_error_up + Z_Ne3O2_error_down)/2,
    Z_R2Ne3_median, (Z_R2Ne3_error_up + Z_R2Ne3_error_down)/2, Z_N2_median, (Z_N2_error_up + Z_N2_error_down)/2, names)


def LzLCS():
    #LzLCS emission lines

    lzlcs_cel_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\Final_LYC_EMISSION_LINES_David.xlsx"
    lzlcs_data_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Strong-line Abundances\lzlcsextras.csv"

    names = pd.read_excel(lzlcs_cel_filepath, usecols = "A", skiprows = 0).to_numpy().flatten()[0:27]

    h_alpha = pd.read_excel(lzlcs_cel_filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()[0:27]
    h_beta = pd.read_excel(lzlcs_cel_filepath, usecols = "Z", skiprows = 0).to_numpy().flatten()[0:27]
   
    o_ii_3727 = pd.read_excel(lzlcs_cel_filepath, usecols = "J", skiprows = 0).to_numpy().flatten()[0:27]

    o_iii_5007 = pd.read_excel(lzlcs_cel_filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()[0:27]
   
    n_ii_6584 = pd.read_excel(lzlcs_cel_filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()[0:27]

    ne_iii_3869 = pd.read_excel(lzlcs_cel_filepath, usecols = "N", skiprows = 0).to_numpy().flatten()[0:27]

    h_alpha_err = pd.read_excel(lzlcs_cel_filepath, usecols="AO", skiprows=0).to_numpy().flatten()[0:27]
    h_beta_err = pd.read_excel(lzlcs_cel_filepath, usecols="AA", skiprows=0).to_numpy().flatten()[0:27]
    o_ii_3727_err = pd.read_excel(lzlcs_cel_filepath, usecols="K", skiprows=0).to_numpy().flatten()[0:27]
    o_iii_5007_err = pd.read_excel(lzlcs_cel_filepath, usecols="AE", skiprows=0).to_numpy().flatten()[0:27]
    n_ii_6584_err = pd.read_excel(lzlcs_cel_filepath, usecols="AQ", skiprows=0).to_numpy().flatten()[0:27]
    ne_iii_3869_err = pd.read_excel(lzlcs_cel_filepath, usecols="O", skiprows=0).to_numpy().flatten()[0:27]

    h_alpha = fix_nan_issues(h_alpha)
    h_alpha_err = fix_nan_issues(h_alpha_err)

    h_beta = fix_nan_issues(h_beta)
    h_beta_err = fix_nan_issues(h_beta_err)

    o_ii_3727 = fix_nan_issues(o_ii_3727)
    o_ii_3727_err = fix_nan_issues(o_ii_3727_err)

    o_iii_5007 = fix_nan_issues(o_iii_5007)
    o_iii_5007_err = fix_nan_issues(o_iii_5007_err)

    n_ii_6584 = fix_nan_issues(n_ii_6584)
    n_ii_6584_err = fix_nan_issues(n_ii_6584_err)

    ne_iii_3869 = fix_nan_issues(ne_iii_3869)
    ne_iii_3869_err = fix_nan_issues(ne_iii_3869_err)

    #Extend strong-line intensities to an array of intensities with the mean at the empirical value
    #And the standard deviation as the error on the empirical value

    h_alpha = np.random.normal(h_alpha[:, None], h_alpha_err[:, None], size = (27, 1000))
    h_beta = np.random.normal(h_beta[:, None], h_beta_err[:, None], size = (27, 1000))
    o_ii_3727 = np.random.normal(o_ii_3727[:, None], o_ii_3727_err[:, None], size = (27, 1000))
    o_iii_5007 = np.random.normal(o_iii_5007[:, None], o_iii_5007_err[:, None], size = (27, 1000))
    n_ii_6584 = np.random.normal(n_ii_6584[:, None], n_ii_6584_err[:, None], size = (27, 1000))
    ne_iii_3869 = np.random.normal(ne_iii_3869[:, None], ne_iii_3869_err[:, None], size = (27, 1000))

    #Direct method metallicity
    direct_Z = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [8], header = 0).to_numpy().flatten()
    direct_Z_err_up = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [9], header = 0).to_numpy().flatten()
    direct_Z_err_down = pd.read_csv(lzlcs_data_filepath, delimiter = ",", usecols = [10], header = 0).to_numpy().flatten()
    direct_Z_err = (direct_Z_err_up + direct_Z_err_down) / 2

    #Strong line metallicities
    #R2 method
    R2 = np.log10(o_ii_3727 / h_beta)
    Z_R2_dist = metallicity(8.00, 0.92, 0.40, 0.17, R2)
    Z_R2_median = np.nanmedian(Z_R2_dist, axis = 1)
    Z_R2_error_up = np.nanpercentile(Z_R2_dist, 84, axis = 1) - Z_R2_median
    Z_R2_error_down = Z_R2_median - np.nanpercentile(Z_R2_dist, 16, axis = 1)

    # O32 method
    O32 = np.log10(o_iii_5007 / o_ii_3727)
    Z_O32_dist = metallicity(8.33, -0.32, 0.08, -0.09, O32)
    Z_O32_median = np.nanmedian(Z_O32_dist, axis = 1)
    Z_O32_error_up = np.nanpercentile(Z_O32_dist, 84, axis = 1) - Z_O32_median
    Z_O32_error_down = Z_O32_median - np.nanpercentile(Z_O32_dist, 16, axis = 1)

    #Ne3O2 method
    Ne3O2 = np.log10(ne_iii_3869 / o_ii_3727)
    Z_Ne3O2_dist = metallicity(7.85, -0.71, -0.26, -0.05, Ne3O2)
    Z_Ne3O2_median = np.nanmedian(Z_Ne3O2_dist, axis = 1)
    Z_Ne3O2_error_up = np.nanpercentile(Z_Ne3O2_dist, 84, axis = 1) - Z_Ne3O2_median
    Z_Ne3O2_error_down = Z_Ne3O2_median - np.nanpercentile(Z_Ne3O2_dist, 16, axis = 1)

    # R2Ne3 method
    R2Ne3 = np.log10((o_ii_3727 + ne_iii_3869) / h_beta)
    Z_R2Ne3_dist = metallicity(7.83, 1.43, 0.00, 0.00, R2Ne3)
    Z_R2Ne3_median = np.nanmedian(Z_R2Ne3_dist, axis = 1)
    Z_R2Ne3_error_up = np.nanpercentile(Z_R2Ne3_dist, 84, axis = 1) - Z_R2Ne3_median
    Z_R2Ne3_error_down = Z_R2Ne3_median - np.nanpercentile(Z_R2Ne3_dist, 16, axis = 1)

    #N2 method
    N2 = np.log10(n_ii_6584 / h_alpha)
    Z_N2_dist = metallicity(9.27, 1.48, 0.86, 0.23, N2)
    Z_N2_median = np.nanmedian(Z_N2_dist, axis = 1)
    Z_N2_error_up = np.nanpercentile(Z_N2_dist, 84, axis = 1) - Z_N2_median
    Z_N2_error_down = Z_N2_median - np.nanpercentile(Z_N2_dist, 16, axis = 1)

    return (
        direct_Z, direct_Z_err, Z_R2_median, (Z_R2_error_up + Z_R2_error_down) / 2, Z_O32_median, (Z_O32_error_up + Z_O32_error_down) / 2,
        Z_Ne3O2_median, (Z_Ne3O2_error_up + Z_Ne3O2_error_down) / 2, Z_R2Ne3_median, (Z_R2Ne3_error_up + Z_R2Ne3_error_down) / 2, Z_N2_median, (Z_N2_error_up + Z_N2_error_down) / 2,
        names)

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