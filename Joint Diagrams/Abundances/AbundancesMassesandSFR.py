import pandas as pd
import pyneb as pn
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit as fit

def nicholls2017(metallicity):
    """Relation to fit log(N/O) with 12+log(O/H)"""
    a = -1.732
    b = 2.19

    ratio = np.log10(10 ** a + 10 ** (metallicity -12 + b))
    return ratio

def haydenpawson2022(stellar_mass):
    """Relation to fit log(N/O) with M*"""
    #Best fitting parameters from paper
    log_n_o_1 = -0.737
    log_n_o_0 = -1.51
    k = 0.95
    log_m_m_0 = 9.55

    log_n_o = log_n_o_1 - ((log_n_o_1 - log_n_o_0)/(1 + 10 ** ((stellar_mass - log_m_m_0)*k)))

    return log_n_o

def classyxii2025(sfr):
    """Relation to fit log(N/O) with SFR for SFR>1, constant for SFR<1"""
    return 0.67*sfr - 1.91

def classyi(mass):
    """Relation to fit SFR with M*"""
    return 0.91*mass - 7.25

def classyimassmetal(mass):
    """Relation to fit metallicity with M* from CLASSY sample"""
    return 0.2*mass + 6.4

def clarke2024(mass):
    """M* - SFR relation for 1.4 < z < 7"""
    m = 0.69
    b = 0.56
    SFR = m * (mass - 9.16) + b

    return SFR

def nakajima2023(mass):
    """High-z MZR for 4<z<10"""
    Z_10 = 8.24
    gamma = 0.25

    metallicity = Z_10 + gamma*(mass - 10)

    return metallicity

def curti2020b(mass, sfr):
    """Fundamental Metallicity Relation between M*, Z, and SFR"""
    Z_0 = 8.779
    m_0 = 10.11
    m_1 = 0.56
    gamma = 0.31
    beta = 2.1

    #This Relation is mixing up logs - fix after dinner
    
    M_0 = m_0 + (sfr * m_1)

    Z = Z_0 - (gamma / beta) * np.log10(1 + (10 ** (beta * (M_0 - mass))))

    return Z

def stantonz2_4(mass):
    """MZR for 2<z<4 from Stanton 26"""
    z = 0.29*mass + 8.14
    return z

def stantonz4_8(mass):
    """MZR for 4<z<8 from Stanton 26"""
    z = 0.30*mass + 8.00
    return z

def fit_fcn(x, a, b):
    return a*x + b

def curvefit(x, y, sigma):
    """Fit linear relations to LzLCS data that uses Berg 2022"""
    mask = np.isfinite(x) & np.isfinite(y) & np.isfinite(sigma) & (sigma >= 0)

    popt, pcov = fit(fit_fcn, xdata=x[mask], ydata=y[mask], sigma=sigma[mask], absolute_sigma=True)
    a, b = popt
    a_err, b_err = np.sqrt(np.diag(pcov))

    return a, a_err, b, b_err

def main():

    classy_abund_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\IonAbundancesCLASSY.csv"
    classy_abund_err_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\AbundanceswerrorsCLASSY.csv"
    classy_prop_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\MassSFRCLASSY.csv"

    lzlcs_abund_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\IonAbundancesLzLCS.csv"
    lzlcs_abund_err_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\AbundanceswerrorsLzLCS.csv"
    lzlcs_mass_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\Final_LYC_EMISSION_LINES_David.xlsx"
    lzlcs_sfr_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\SFRLzLCS.csv"

    background_abund_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\Sample_NO_abundances_Literature.xlsx"

    high_z_filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\Abundances\David_highz-sample.xlsx"

    classy_metal = pd.read_csv(classy_abund_filepath, delimiter=",", usecols = [0], header = 0).to_numpy().flatten()[0:45]
    classy_metal_err_u = pd.read_csv(classy_abund_err_filepath, delimiter=",", usecols = [0], header=0).to_numpy().flatten()
    classy_metal_err_d = pd.read_csv(classy_abund_err_filepath, delimiter=",", usecols = [1], header=0).to_numpy().flatten()

    classy_n_o = pd.read_csv(classy_abund_filepath, delimiter=",", usecols = [1], header = 0).to_numpy().flatten()[0:45]
    classy_n_o_err_u = pd.read_csv(classy_abund_err_filepath, delimiter=",", usecols = [2], header=0).to_numpy().flatten()
    classy_n_o_err_d = pd.read_csv(classy_abund_err_filepath, delimiter=",", usecols = [3], header=0).to_numpy().flatten()

    classy_mass = pd.read_csv(classy_prop_filepath, delimiter=",", usecols=[6], header = 0).to_numpy().flatten()
    classy_sfr = pd.read_csv(classy_prop_filepath, delimiter=",", usecols=[7], header = 0).to_numpy().flatten()

    lzlcs_metal = pd.read_csv(lzlcs_abund_filepath, delimiter=",", usecols = [0], header = 0).to_numpy().flatten()
    lzlcs_metal_err_u = pd.read_csv(lzlcs_abund_err_filepath, delimiter=",", usecols = [1], header=0).to_numpy().flatten()
    lzlcs_metal_err_d = pd.read_csv(lzlcs_abund_err_filepath, delimiter=",", usecols = [2], header=0).to_numpy().flatten()

    lzlcs_n_o = pd.read_csv(lzlcs_abund_filepath, delimiter=",", usecols = [1], header = 0).to_numpy().flatten()
    lzlcs_n_o_err_u = pd.read_csv(lzlcs_abund_err_filepath, delimiter=",", usecols = [4], header=0).to_numpy().flatten()
    lzlcs_n_o_err_d = pd.read_csv(lzlcs_abund_err_filepath, delimiter=",", usecols = [5], header=0).to_numpy().flatten()

    lzlcs_mass = pd.read_excel(lzlcs_mass_filepath, usecols="AX", skiprows=0).to_numpy().flatten()
    lzlcs_mass_err = pd.read_excel(lzlcs_mass_filepath, usecols="AY", skiprows=0).to_numpy().flatten()

    lzlcs_sfr = pd.read_csv(lzlcs_sfr_filepath, delimiter=",", usecols = [2], header = 0).to_numpy().flatten()
    lzlcs_sfr_err = pd.read_csv(lzlcs_sfr_filepath, delimiter=",", usecols = [3], header = 0).to_numpy().flatten()

    background_metal = pd.read_excel(background_abund_filepath, usecols = "B", skiprows = 0).to_numpy().flatten()
    background_metal_err = pd.read_excel(background_abund_filepath, usecols = "C", skiprows = 0).to_numpy().flatten()
    background_n_o = pd.read_excel(background_abund_filepath, usecols = "D", skiprows = 0).to_numpy().flatten()
    background_n_o_err = pd.read_excel(background_abund_filepath, usecols = "E", skiprows = 0).to_numpy().flatten()

    high_z_mass = pd.read_excel(high_z_filepath, usecols = "C", skiprows = 0).to_numpy().flatten()
    high_z_mass_err_up = pd.read_excel(high_z_filepath, usecols = "D", skiprows = 0).to_numpy().flatten()
    high_z_mass_err_down = pd.read_excel(high_z_filepath, usecols = "E", skiprows = 0).to_numpy().flatten()
    high_z_mass_err = (high_z_mass_err_down + high_z_mass_err_up) / 2
    high_z_sfr = pd.read_excel(high_z_filepath, usecols = "F", skiprows = 0).to_numpy().flatten()
    high_z_sfr_err = pd.read_excel(high_z_filepath, usecols = "G", skiprows = 0).to_numpy().flatten()
    high_z_metal = pd.read_excel(high_z_filepath, usecols = "H", skiprows = 0).to_numpy().flatten()
    high_z_metal_err = pd.read_excel(high_z_filepath, usecols = "I", skiprows = 0).to_numpy().flatten()
    high_z_n_o = pd.read_excel(high_z_filepath, usecols = "J", skiprows = 0).to_numpy().flatten()
    high_z_n_o_err = pd.read_excel(high_z_filepath, usecols = "K", skiprows = 0).to_numpy().flatten()
                       
    classy_metal_err = (classy_metal_err_d + classy_metal_err_u) / 2
    classy_n_o_err = (classy_n_o_err_d + classy_n_o_err_u) / 2
    lzlcs_metal_err = (lzlcs_metal_err_d + lzlcs_metal_err_u) / 2
    lzlcs_n_o_err = (lzlcs_n_o_err_d + lzlcs_n_o_err_u) / 2

    #Metallicity vs. N/O

    xnicholls = np.linspace(6.9, 9.0, 1000)
    ynicholls = nicholls2017(xnicholls)

    plt.scatter(high_z_metal, high_z_n_o, s=20, color = "goldenrod", alpha = 0.3, label = "z>6")
    plt.errorbar(high_z_metal, high_z_n_o, xerr=high_z_metal_err, yerr = high_z_n_o_err, 
                 fmt = "none", color = "goldenrod", alpha = 0.3)
    plt.scatter(background_metal, background_n_o, s = 20, ls = "", color = "silver")
    plt.scatter(classy_metal, classy_n_o, s=20, color="slateblue", label="CLASSY (z~0)")
    plt.errorbar(classy_metal, classy_n_o, xerr=classy_metal_err, yerr=classy_n_o_err,
             fmt='none', ecolor="slateblue")
    plt.scatter(lzlcs_metal, lzlcs_n_o, s=20, color="salmon", label="LzLCS(z~0.3)")
    plt.errorbar(lzlcs_metal, lzlcs_n_o, xerr=lzlcs_metal_err, yerr=lzlcs_n_o_err,
             fmt='none', ecolor="salmon")
    plt.plot(xnicholls, ynicholls, color = "darkgreen", label = "Nicholls+2017")
    plt.xlabel(r"$12 + log_{10}(O/H)$", fontsize = 12)
    plt.ylabel(r"$log_{10}(N/O)$", fontsize = 12)
    plt.xlim(6.9, 9)
    plt.ylim(-2, 0.25)
    plt.tight_layout()
    plt.legend()
    plt.savefig("NO-OH Relation.png")
    plt.show()

    #Metallicity vs Mass

    mass = np.linspace(5.5, 10.5, 1000)
    mass_nakajima = np.linspace(7.5, 9.5, 1000)
    mass_stanton = np.linspace(8.0, 10.3, 1000)
    z_berg = classyimassmetal(mass)
    z_nakajima = nakajima2023(mass_nakajima)
    z_stanton24 = stantonz2_4(mass_stanton)
    z_stanton48 = stantonz4_8(mass_stanton)

    #LzLCS linear fit
    a, a_err, b, b_err = curvefit(lzlcs_mass, lzlcs_metal, lzlcs_metal_err)
    z_lzlcs = fit_fcn(mass, a, b)

    plt.scatter(high_z_mass, high_z_metal, s=20, color = "goldenrod", alpha = 0.3, label = "z>3")
    plt.errorbar(high_z_mass, high_z_metal, xerr=high_z_mass_err, yerr = high_z_metal_err, 
                 fmt = "none", color = "goldenrod", alpha = 0.3)
    plt.scatter(classy_mass, classy_metal, s = 20, ls = "", color = "slateblue", label = "CLASSY(z~0)")
    plt.errorbar(classy_mass, classy_metal, yerr = classy_metal_err, fmt = "none", ecolor = "slateblue")
    plt.scatter(lzlcs_mass, lzlcs_metal, s = 20, ls = "", color = "salmon", label = "LzLCS(z~0.3)")
    plt.errorbar(lzlcs_mass, lzlcs_metal, xerr = lzlcs_mass_err, yerr = lzlcs_metal_err, fmt = "none", ecolor = "salmon")
    plt.plot(mass, z_berg, color = "darkgreen", label = "Berg+2022 (z~0)")
    plt.plot(mass_nakajima, z_nakajima, color = "purple", label = "Nakajima+2023 (4<z<10)")
    #plt.plot(mass_stanton, z_stanton24, color = "teal", label = "Stanton+2026 (2<z<4)")
    #plt.plot(mass_stanton, z_stanton48, color = "grey", label = "Stanton+2026 (4<z<8)")
    plt.plot(mass, z_lzlcs, color = "olive", label = "This work (z~0)")
    plt.xlim(5.5, 11)
    plt.ylim(6.9, 9.5)
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)", fontsize = 12)
    plt.ylabel(r"$12 + log_{10}(O/H)$", fontsize = 12)
    plt.legend()
    plt.tight_layout()
    plt.savefig("MZR.png")
    plt.show()

    print(f"The M-Z fit for LzLCS returned a gradient of {a} +-{a_err} and an intercept of {b}+-{b_err}")

    #Metallicity vs SFR

    #xcurti = np.linspace(-3, 3, 1000)
    #ycurti6 = curti2020b(6, xcurti)
    #ycurti7 = curti2020b(7, xcurti)
    #ycurti8 = curti2020b(8, xcurti)
    #ycurti9 = curti2020b(9, xcurti)
    #ycurti10 = curti2020b(10, xcurti)
    plt.scatter(high_z_sfr, high_z_metal, s=20, color = "goldenrod", alpha = 0.3, label = "z>3")
    plt.errorbar(high_z_sfr, high_z_metal, xerr=high_z_sfr_err, yerr = high_z_metal_err, 
                 fmt = "none", color = "goldenrod", alpha = 0.3)
    plt.scatter(classy_sfr, classy_metal, s = 20, ls = "", color = "slateblue", label = "CLASSY(z~0)")
    plt.errorbar(classy_sfr, classy_metal, yerr = classy_metal_err, fmt = "none", ecolor = "slateblue")
    plt.scatter(lzlcs_sfr, lzlcs_metal, s = 20, ls = "", color = "salmon", label = "LzLCS(z~0.3)")
    plt.errorbar(lzlcs_sfr, lzlcs_metal, xerr = lzlcs_sfr_err, yerr = lzlcs_metal_err, fmt = "none", ecolor = "salmon")
    
    #plt.plot(xcurti, ycurti6, color = "springgreen", label = r"Curti 2020 $\log_{10}M* = 6$")
    #plt.plot(xcurti, ycurti7, color = "limegreen", label = r"Curti 2020 $\log_{10}M* = 7$")
    #plt.plot(xcurti, ycurti8, color = "seagreen", label = r"Curti 2020 $\log_{10}M* = 8$")
    #plt.plot(xcurti, ycurti9, color = "forestgreen", label = r"Curti 2020 $\log_{10}M* = 9$")
    #plt.plot(xcurti, ycurti10, color = "darkgreen", label = r"Curti 2020 $\log_{10}M* = 10$")
    plt.xlim(-3, 3)
    plt.ylim(6.9, 9.5)
    plt.xlabel(r"$log_{10}$ of star-formation rate in galaxy ($M_{\odot} yr^{-1}$)", fontsize = 12)
    plt.ylabel(r"$12 + log_{10}(O/H)$", fontsize = 12)
    #plt.legend(loc = "upper left", ncols = 2, fontsize = 8)
    plt.legend()
    plt.tight_layout()
    plt.savefig("SFRMetallicity.png")
    plt.show()

    #N/O vs. Mass

    xhaydenpawson = np.linspace(5, 11, 100)
    yhaydenpawson = haydenpawson2022(xhaydenpawson)

    plt.scatter(high_z_mass, high_z_n_o, s=20, color = "goldenrod", alpha = 0.3, label = "z>6")
    plt.errorbar(high_z_mass, high_z_n_o, xerr=high_z_mass_err, yerr = high_z_n_o_err, 
                 fmt = "none", color = "goldenrod", alpha = 0.3)
    plt.scatter(classy_mass, classy_n_o, s = 20, ls = "", color = "slateblue", label = "CLASSY(z~0)")
    plt.errorbar(classy_mass, classy_n_o, yerr = classy_metal_err, fmt = "none", ecolor = "slateblue")
    plt.scatter(lzlcs_mass, lzlcs_n_o, s = 20, ls = "", color = "salmon", label = "LzLCS(z~0.3)")
    plt.errorbar(lzlcs_mass, lzlcs_n_o, xerr = lzlcs_mass_err, yerr = lzlcs_n_o_err, fmt = "none", ecolor = "salmon")
    plt.plot(xhaydenpawson, yhaydenpawson, color = "darkgreen", label = "Hayden-Pawson+2022 (z~0)")
    plt.xlim(5,11)
    #plt.ylim(-2.2, -0.5)
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)", fontsize = 12)
    plt.ylabel(r"$log_{10}(N/O)$", fontsize = 12)
    plt.legend()
    plt.tight_layout()
    plt.savefig("MNO.png")
    plt.show()

    #N/O vs SFR

    low_sfr = np.linspace(-3, 1, 1000)
    high_sfr = np.linspace(1, 3, 1000)
    classyxii_low = np.full(1000, -1.38)
    classyxii_high = classyxii2025(high_sfr)

    plt.scatter(high_z_sfr, high_z_n_o, s=20, color = "goldenrod", alpha = 0.3, label = "z>6")
    plt.errorbar(high_z_sfr, high_z_n_o, xerr=high_z_sfr_err, yerr = high_z_n_o_err, 
                 fmt = "none", color = "goldenrod", alpha = 0.3)
    plt.scatter(classy_sfr, classy_n_o, s = 20, ls = "", color = "slateblue", label = "CLASSY(z~0)")
    plt.errorbar(classy_sfr, classy_n_o, yerr = classy_n_o_err, fmt = "none", ecolor = "slateblue")
    plt.scatter(lzlcs_sfr, lzlcs_n_o, s = 20, ls = "", color = "salmon", label = "LzLCS(z~0.3)")
    plt.errorbar(lzlcs_sfr, lzlcs_n_o, xerr = lzlcs_sfr_err, yerr = lzlcs_n_o_err, fmt = "none", ecolor = "salmon")
    plt.plot(low_sfr, classyxii_low, color = "darkgreen", label = "A-C+2025 (z~0)")
    plt.plot(high_sfr, classyxii_high, color = "darkgreen")
    plt.xlim(-3,3)
    #plt.ylim(-2.2, -0.5)
    plt.xlabel(r"$log_{10}$ of star-formation rate in galaxy ($M_{\odot} yr^{-1}$)", fontsize = 12)
    plt.ylabel(r"$log_{10}(N/O)$", fontsize = 12)
    plt.legend()
    plt.tight_layout()
    plt.savefig("SFRNO.png")
    plt.show()

    #M vs SFR

    xmass = np.linspace(5, 11, 1000)
    sfrberg = classyi(xmass)
    sfrclarke = clarke2024(xmass)
    a, a_err, b, b_err = curvefit(lzlcs_mass, lzlcs_sfr, lzlcs_sfr_err)
    sfrlzlcs = fit_fcn(mass, a, b)

    plt.scatter(high_z_mass, high_z_sfr, s=20, color = "goldenrod", alpha = 0.3, label = "z>3")
    plt.errorbar(high_z_mass, high_z_sfr, xerr=high_z_mass_err, yerr = high_z_sfr_err, 
                 fmt = "none", color = "goldenrod", alpha = 0.3)
    plt.scatter(classy_mass, classy_sfr, s = 20, ls = "", color = "slateblue", label = "CLASSY(z~0)")
    plt.errorbar(classy_mass, classy_sfr, fmt = "none", ecolor = "slateblue")
    plt.scatter(lzlcs_mass, lzlcs_sfr, s = 20, ls = "", color = "salmon", label = "LzLCS(z~0)")
    plt.errorbar(lzlcs_mass, lzlcs_sfr, xerr = lzlcs_mass_err, yerr = lzlcs_sfr_err, fmt = "none", ecolor = "salmon")
    plt.plot(xmass, sfrberg, color = "darkgreen", label = "Berg+2022 (z~0)")
    plt.plot(xmass, sfrclarke, color = "lightgreen", label = "Clarke+2024 (1.4<z<7)")
    plt.plot(xmass, sfrlzlcs, color = "olive", label = "This work (z~0)")
    plt.xlim(5,11)
    plt.ylim(-3, 3)
    plt.xlabel(r"$log_{10}$ of total stellar mass in galaxy ($M_{\odot}$)", fontsize = 12)
    plt.ylabel(r"$log_{10}$ of star-formation rate in galaxy ($M_{\odot} yr^{-1}$)", fontsize = 12)
    plt.legend()
    plt.tight_layout()
    plt.savefig("SFRM.png")
    plt.show()

    print(f"The gradient of the M-SFR relation fit for LzLCS is {a}+-{a_err} and the intercept is {b}+-{b_err}")













main()

