import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

def fix_nan_issues(array):
    """Replace missing data in the LzLCS dataset from -999.999 to nan"""
    array[array == -999.999] = np.nan
    return array

def main():
    """Extracts necessary emission lines, use getCrossTemDen to calculate T_e in low and high-
    ionisation regions and plot them together, optionally including expanded T_e datasets for galaxies
    without necessary emission lines using Garnett's 1992 formula"""
    filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Final_LYC_EMISSION_LINES_David.xlsx"

    O2 = pn.Atom("O", 2)
    O3 = pn.Atom("O", 3)
    N2 = pn.Atom("N", 2)
    S2 = pn.Atom("S", 2)

    diags = pn.Diagnostics()

    o_iii_5007 = pd.read_excel(filepath, usecols = "AD", skiprows = 0).to_numpy().flatten()
    o_iii_4363 = pd.read_excel(filepath, usecols = "V", skiprows = 0).to_numpy().flatten()
    s_ii_6717 = pd.read_excel(filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()
    s_ii_6731 = pd.read_excel(filepath, usecols = "AT", skiprows = 0).to_numpy().flatten()

    o_iii_5007 = fix_nan_issues(o_iii_5007)
    o_iii_4363 = fix_nan_issues(o_iii_4363)
    s_ii_6717 = fix_nan_issues(s_ii_6717)
    s_ii_6731 = fix_nan_issues(s_ii_6731)

    #[OII]7320,30 do not exist in LzLCS file, use Garnett formula to estimate temperature

    oiii_ratio = o_iii_4363/o_iii_5007
    sii_ratio = s_ii_6731/s_ii_6717

    print(oiii_ratio)
    print(sii_ratio)

    #Use getCrossTemDen to compute densities
    n_e = diags.getCrossTemDen("[OIII] 4363/5007", '[SII] 6731/6716', oiii_ratio, sii_ratio)[1]
    #If no density given, default to 100 cm^-3
    n_e = np.nan_to_num(n_e, nan = 100)

    #Calculate temperatures of regions with OIII data
    o_iii_T_e = O3.getTemDen(int_ratio = oiii_ratio, den = n_e, wave1 = 4363, wave2 = 5007)[0:27]
    #Use Garnett to derive OII data
    o_ii_T_e = 0.7 * o_iii_T_e + 3000

    print(f"The number of galaxies where the OIII diagnostic works is {np.sum(~np.isnan(o_iii_T_e))}/27)")

    #Plot galaxy temperature data 
    #Errors
    errpath = r"C:\Users\drcla\OneDrive\Senior Honours Project\LzLCS\Diagnostics\Tempswerrors.csv"
    Tiii_up = pd.read_csv(errpath, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()
    Tiii_down = pd.read_csv(errpath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
    Tiii_err = np.stack((Tiii_up, Tiii_down), axis = 0)

    Tii_up = pd.read_csv(errpath, delimiter = ",", usecols = [4], header = 0).to_numpy().flatten()
    Tii_down = pd.read_csv(errpath, delimiter = ",", usecols = [5], header = 0).to_numpy().flatten()
    Tii_err = np.stack((Tii_up, Tii_down), axis = 0)
      

    #Data points that come from the emission lines
    plt.errorbar(o_iii_T_e, o_ii_T_e, yerr = Tii_err, xerr= Tiii_err,  ls = "", marker = "x", color = "r")
    #Data points that come from Garnett's formula
    #plt.errorbar(o_iii_T_e_exp[garnett_mask_1], o_ii_T_e_exp[garnett_mask_1], yerr = [Tii_down[garnett_mask_1], Tii_up[garnett_mask_1]], xerr= [Tiii_down[garnett_mask_1], Tiii_up[garnett_mask_1]], ls = "", marker = "x", color = "g", label = "Garnett")
    #plt.errorbar(o_iii_T_e_exp[garnett_mask_2], o_ii_T_e_exp[garnett_mask_2], yerr = [Tii_down[garnett_mask_2], Tii_up[garnett_mask_2]], xerr= [Tiii_down[garnett_mask_2], Tiii_up[garnett_mask_2]], ls = "", marker = "x", color = "g")
    plt.axline(xy1 = (0, 3000), slope = 0.7, color = "b" , label = "Garnett 1992 \n T_e[OII] = 0.7T_e[OIII] + 3000K" )
    plt.xlim(6000, 20000)
    plt.ylim(6000, 20000)
    plt.xlabel("T_e[OIII] (K)")
    plt.ylabel("T_e[OII] (K)")
    plt.title("T_e[OIII]_vs_T_e[OII]")
    plt.legend()
    plt.savefig("Tempswoformula")
    #plt.show()


if __name__ == "__main__":
     main()