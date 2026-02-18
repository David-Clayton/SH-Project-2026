import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

filepathion = r"C:\Users\drcla\OneDrive\Senior Honours Project\Abundances\IonAbundances.csv"
filepathmass = r"C:\Users\drcla\OneDrive\Senior Honours Project\Abundances\classy_sample_prop.csv"

stellar_mass = pd.read_csv(filepathmass, delimiter = ",", usecols = [6], header = 0).to_numpy().flatten()
metallicity = pd.read_csv(filepathion, delimiter = ",", usecols = [0], header = 0).to_numpy().flatten()

#Arrays different lengths - truncate excess nans at end of metallicity 
metallicity = metallicity[0:len(stellar_mass)]

#Plot
plt.scatter(stellar_mass, metallicity, marker = "s", color = "red")
plt.axline(xy1 = (0, 6.4), slope = 0.2, color = "green", label = "12+log(O/H) = 0.2M*+6.4")
plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)")
plt.ylabel(r"12 + $log_{10}(O/H)$")
plt.xlim(5, 11)
plt.legend()
plt.title("Relationship between total stellar mass \n and metallicity of galaxies")
plt.savefig("MassvMetallicity")
plt.show()