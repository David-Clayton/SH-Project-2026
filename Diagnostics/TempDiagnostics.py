import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit
filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Diagnostics\Final_CLASSY_EMISSION_LINES_David.xlsx"

O2 = pn.Atom("O", 2)
O3 = pn.Atom("O", 3)
N2 = pn.Atom("N", 2)
S2 = pn.Atom("S", 2)

diags = pn.Diagnostics()

o_iii_5007 = pd.read_excel(filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()
o_iii_4363 = pd.read_excel(filepath, usecols = "R", skiprows = 0).to_numpy().flatten()
o_ii_3727 = pd.read_excel(filepath, usecols = "B", skiprows = 0).to_numpy().flatten()
o_ii_3729 = pd.read_excel(filepath, usecols = "F", skiprows = 0).to_numpy().flatten()
o_ii_7320 = pd.read_excel(filepath, usecols = "CB", skiprows = 0).to_numpy().flatten()
o_ii_7330 = pd.read_excel(filepath, usecols = "CF", skiprows = 0).to_numpy().flatten()
s_ii_6717 = pd.read_excel(filepath, usecols = "BT", skiprows = 0).to_numpy().flatten()
s_ii_6731 = pd.read_excel(filepath, usecols = "BX", skiprows = 0).to_numpy().flatten()

 #errors

o_iii_5007_err_up = pd.read_excel(filepath, usecols = "AW", skiprows = 0).to_numpy().flatten()
o_iii_4363_err_up = pd.read_excel(filepath, usecols = "S", skiprows = 0).to_numpy().flatten()
s_ii_6717_err_up = pd.read_excel(filepath, usecols = "BU", skiprows = 0).to_numpy().flatten()
s_ii_6731_err_up = pd.read_excel(filepath, usecols = "BY", skiprows = 0).to_numpy().flatten()

    
o_iii_5007_err_down = pd.read_excel(filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()
s_ii_6717_err_down = pd.read_excel(filepath, usecols = "BV", skiprows = 0).to_numpy().flatten()
s_ii_6731_err_down = pd.read_excel(filepath, usecols = "BZ", skiprows = 0).to_numpy().flatten()

oiii_ratio = o_iii_4363/o_iii_5007
oii_ratio = (o_ii_3727 + o_ii_3729) / (o_ii_7320 + o_ii_7330)
sii_ratio = s_ii_6731/s_ii_6717

#print(sii_ratio)
#Use getCrossTemDen to compute densities
n_e = diags.getCrossTemDen("[OIII] 4363/5007", '[SII] 6731/6716', oiii_ratio, sii_ratio)[1]
#If no density given, default to 100 cm^-3
n_e = np.nan_to_num(n_e, nan = 100)

#Calculate temperatures of regions with OIII & OII data
o_iii_T_e = O3.getTemDen(int_ratio = oiii_ratio, den = n_e, wave1 = 4363, wave2 = 5007)[0:45]
o_ii_T_e = O2.getTemDen(int_ratio = oii_ratio, den = n_e, to_eval = "(L(3726)+L(3729))/(L(7319)+L(7320)+L(7331)+L(7333))")[0:45]

#To determine number of galaxies where both intensities can be measured, add arrays together. Any number + nan = nan
o_ii_and_iii = o_iii_T_e + o_ii_T_e

#Use equation T_e[OII] = 0.7T_e[OIII] + 3000K to expand the datasets 
o_iii_exp = (o_ii_T_e - 3000) / 0.7
o_ii_exp = 0.7 * o_iii_T_e + 3000

o_iii_T_e_exp = np.nan_to_num(o_iii_T_e, nan = o_iii_exp)
o_ii_T_e_exp = np.nan_to_num(o_ii_T_e, nan = o_ii_exp)
o_ii_and_iii_exp = o_ii_T_e_exp + o_iii_T_e_exp


#print(f"The number of galaxies where the OIII diagnostic works is {np.sum(~np.isnan(o_iii_T_e))}/45, \
      #increasing to {np.sum(~np.isnan(o_iii_T_e_exp))}/45 when the equation from Garnett (1992) is used.")

#print(f"The number of galaxies where the OII diagnostic works is {np.sum(~np.isnan(o_ii_T_e))}/45, \
      #increasing to {np.sum(~np.isnan(o_ii_T_e_exp))}/45 when the equation from Garnett (1992) is used.")

#print(f"The number of galaxies where both the OIII and OII diagnostics work is {np.sum(~np.isnan(o_ii_and_iii))}/45, \
      #increasing to {np.sum(~np.isnan(o_ii_and_iii_exp))}/45 when the equation from Garnett (1992) is used.")

#Plot galaxy temperature data 

#Errors
errpath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Diagnostics\Tempswerrors.csv"
Tiii_up = pd.read_csv(errpath, delimiter = ",", usecols = [1], header = 0).to_numpy().flatten()
Tiii_down = pd.read_csv(errpath, delimiter = ",", usecols = [2], header = 0).to_numpy().flatten()
Tii_up = pd.read_csv(errpath, delimiter = ",", usecols = [4], header = 0).to_numpy().flatten()
Tii_down = pd.read_csv(errpath, delimiter = ",", usecols = [5], header = 0).to_numpy().flatten()

#Boolean conditions - if False, datapoint comes from emission lines
#If True, data either doesn't exist or expanded from Garnett

o_iii_garn = np.isnan(o_iii_T_e)
o_ii_garn = np.isnan(o_ii_T_e)

#Masks
emission_line_mask = ~o_iii_garn & ~o_ii_garn
garnett_mask_1 = o_iii_garn & ~o_ii_garn
garnett_mask_2 = ~o_iii_garn & o_ii_garn

print(len(o_ii_T_e[emission_line_mask]))
print(len(Tii_down[emission_line_mask]))

#Data points that come from the emission lines
plt.errorbar(o_iii_T_e[emission_line_mask], o_ii_T_e[emission_line_mask], yerr = [Tii_down[emission_line_mask], Tii_up[emission_line_mask]], xerr= [Tiii_down[emission_line_mask], Tiii_up[emission_line_mask]],  ls = "", marker = "x", color = "r", label = "Emission lines")
#Data points that come from Garnett's formula
#plt.errorbar(o_iii_T_e_exp[garnett_mask_1], o_ii_T_e_exp[garnett_mask_1], yerr = [Tii_down[garnett_mask_1], Tii_up[garnett_mask_1]], xerr= [Tiii_down[garnett_mask_1], Tiii_up[garnett_mask_1]], ls = "", marker = "x", color = "g", label = "Garnett")
#plt.errorbar(o_iii_T_e_exp[garnett_mask_2], o_ii_T_e_exp[garnett_mask_2], yerr = [Tii_down[garnett_mask_2], Tii_up[garnett_mask_2]], xerr= [Tiii_down[garnett_mask_2], Tiii_up[garnett_mask_2]], ls = "", marker = "x", color = "g")
plt.axline(xy1 = (0, 3000), slope = 0.7, color = "b" , label = "T_e[OII] = 0.7T_e[OIII] + 3000K" )
plt.xlim(6000, 20000)
plt.ylim(6000, 20000)
plt.xlabel("T_e[OIII] (K)")
plt.ylabel("T_e[OII] (K)")
plt.title("T_e[OIII]_vs_T_e[OII] Using data from \n emission lines")
plt.legend()
plt.savefig("Tempswoformula")
plt.show()

#def fit_fcn(a, b, x):
    #return a*x + b
#o_iii_T_e_exp = np.nan_to_num(o_iii_T_e_exp)
#o_ii_T_e_exp = np.nan_to_num(o_ii_T_e_exp)

#fit_params = fit(fit_fcn, o_iii_T_e_exp, o_ii_T_e_exp)
#print(fit_params)