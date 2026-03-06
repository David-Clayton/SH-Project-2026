import pandas as pd
import pyneb as pn
import numpy as np

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