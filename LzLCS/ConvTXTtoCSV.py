import pandas as pd

# Define column specifications from the byte positions in the header
colspecs = [
    (0, 14),   # ID
    (15, 21),  # logSFR
    (22, 27),  # e_logSFR
    (28, 32),  # ne
    (33, 37),  # e_ne
    (38, 43),  # Te
    (44, 48),  # e_Te
    (49, 54),  # logO
    (55, 60)   # e_logO
]

names = ['ID', 'logSFR', 'e_logSFR', 'ne', 'e_ne', 'Te', 'e_Te', 'logO', 'e_logO']

# Read the file, skipping the header lines
data = pd.read_fwf('apjsad7bb9t4_mrt.txt', 
                 colspecs=colspecs, 
                 names=names,
                 skiprows=31)  # Skip header lines

data.to_csv("SFR.csv")

