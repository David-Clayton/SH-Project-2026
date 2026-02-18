import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Abundances\Final_CLASSY_EMISSION_LINES_David.xlsx"

O2 = pn.Atom("O", 2)
O3 = pn.Atom("O", 3)
N2 = pn.Atom("N", 2)

diags = pn.Diagnostics()

h_beta = pd.read_excel(filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()
o_ii_3727 = pd.read_excel(filepath, usecols = "B", skiprows = 0).to_numpy().flatten()
o_ii_3729 = pd.read_excel(filepath, usecols = "F", skiprows = 0).to_numpy().flatten()
o_ii_7320 = pd.read_excel(filepath, usecols = "CB", skiprows = 0).to_numpy().flatten()
o_ii_7330 = pd.read_excel(filepath, usecols = "CF", skiprows = 0).to_numpy().flatten()
o_iii_5007 = pd.read_excel(filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()
o_iii_4959 = pd.read_excel(filepath, usecols = "AR", skiprows = 0).to_numpy().flatten()
o_iii_4363 = pd.read_excel(filepath, usecols = "R", skiprows = 0).to_numpy().flatten()
n_ii_6584 = pd.read_excel(filepath, usecols = "BP", skiprows = 0).to_numpy().flatten()
s_ii_6717 = pd.read_excel(filepath, usecols = "BT", skiprows = 0).to_numpy().flatten()
s_ii_6731 = pd.read_excel(filepath, usecols = "BX", skiprows = 0).to_numpy().flatten()

#Intensity ratios for abundances
o_iii_ratio = (o_iii_4959 + o_iii_5007) / h_beta
o_ii_ratio_1 = (o_ii_3727 + o_ii_3729) / h_beta #Primary
o_ii_ratio_2 = (o_ii_7320 + o_ii_7330) / h_beta #Backup if above lines not present
n_ii_ratio = n_ii_6584 / h_beta

#Intensity ratios for physical conditions
#Temperature
oiii_ratio = o_iii_4363/o_iii_5007
oii_ratio = (o_ii_3727 + o_ii_3729) / (o_ii_7320 + o_ii_7330)
#Density
sii_ratio = s_ii_6731/s_ii_6717

"""Following code reused from TempDiagnostics.py"""

#Use getCrossTemDen to compute densities
n_e = diags.getCrossTemDen("[OIII] 4363/5007", '[SII] 6731/6716', oiii_ratio, sii_ratio)[1]
#If no density given, default to 100 cm^-3
#n_e = np.nan_to_num(n_e, nan = 100)
print(n_e)
#Calculate temperatures of regions with OIII & OII data
o_iii_T_e = O3.getTemDen(int_ratio = oiii_ratio, den = n_e, wave1 = 4363, wave2 = 5007)
o_ii_T_e = O2.getTemDen(int_ratio = oii_ratio, den = n_e, to_eval = "(L(3726)+L(3729))/(L(7319)+L(7320)+L(7331)+L(7333))")

#Use equation T_e[OII] = 0.7T_e[OIII] + 3000K to expand the datasets 
o_iii_exp = (o_ii_T_e - 3000) / 0.7


o_iii_T_e_exp = np.nan_to_num(o_iii_T_e, nan = o_iii_exp)
"""Don't use OII emission lines directly - use Garnett formula on OIII temps 
OIII T data expanded with Garnett formula"""
o_ii_T_e_exp = 0.7 * o_iii_T_e_exp + 3000


"""End of reused code"""

o_ii_T_e = o_ii_T_e_exp
o_iii_T_e = o_iii_T_e_exp

#Compute abundances
#O+ / H+
#Primary abundance diagnostic 
o_ii_abundance1 = O2.getIonAbundance(o_ii_ratio_1, tem = o_ii_T_e, den = n_e,  to_eval = "L(3726)+L(3729)", Hbeta = 1)
#Backup
o_ii_abundance2 = O2.getIonAbundance(o_ii_ratio_2, tem = o_ii_T_e, den = n_e, to_eval = "(L(7319)+L(7320)+L(7331)+L(7333))", Hbeta = 1)

#O++ / H+
o_iii_abundance = O3.getIonAbundance(o_iii_ratio, tem = o_iii_T_e, den = n_e, to_eval = "L(4959)+L(5007)", Hbeta = 1)
print(o_iii_abundance)
#N+ / H+
n_ii_abundance = N2.getIonAbundance(n_ii_ratio, tem = o_ii_T_e, den = n_e, to_eval = "L(6584)", Hbeta = 1)

#Use backup diagnostic to expand OII dataset
o_ii_abundance = np.nan_to_num(o_ii_abundance1, nan = o_ii_abundance2)
print(o_ii_abundance)
6
#Combine O+ and O++ abundances to get total O abundance
#O/H
o_h = (o_ii_abundance + o_iii_abundance) 
#N/O ~ N+/O+
n_o = n_ii_abundance / o_ii_abundance 

#Metallicity formula
metallicity = np.log10(o_h) + 12
log_n_o = np.log10(n_o)

#Plot to compare to classy xii fig 2
plt.scatter(metallicity, log_n_o, marker = "^", color = "b")
plt.xlabel("12 + log(O/H)")
plt.ylabel("log(N/O)")
plt.title("Metallicity")
plt.savefig("Metallicity")
plt.show()

#Count how many points are in scatter plot
print(np.sum(~np.isnan(metallicity * n_o)))

ion_data = np.column_stack((metallicity, log_n_o))
np.savetxt("IonAbundances.csv", ion_data, delimiter=",", header = "12 + log(O/H) , log(N/O)")