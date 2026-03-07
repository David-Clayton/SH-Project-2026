import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

### Kauffmann 2003 empiric starburst line
def n2kauffmann(n2ha):
    return 0.61 / (n2ha - 0.05) + 1.3
### Kewley 2001 theoretical starburst lines
def n2kewley(n2ha):
    return 0.61 / (n2ha - 0.47) + 1.19
def s2kewley(s2ha):
    return 0.72 / (s2ha - 0.32) + 1.30
def o1kewley(o1ha):
    return 0.73 / (o1ha + 0.59) + 1.33

def extract_and_plot():
    """Extracts the necessary emission line spectra and plots them to replicate fig. 2
    of CLASSY VIII"""

    filepath = r"C:\Users\drcla\OneDrive\Senior Honours Project\BPT diagrams\Final_CLASSY_EMISSION_LINES_David.xlsx"

    o_iii_5007 = pd.read_excel(filepath, usecols = "AV", skiprows = 0).to_numpy().flatten()
    n_ii_6584 = pd.read_excel(filepath, usecols = "BP", skiprows = 0).to_numpy().flatten()
    s_ii_6717 = pd.read_excel(filepath, usecols = "BT", skiprows = 0).to_numpy().flatten()
    s_ii_6731 = pd.read_excel(filepath, usecols = "BX", skiprows = 0).to_numpy().flatten()
    o_i_6300 = pd.read_excel(filepath, usecols = "BD", skiprows = 0).to_numpy().flatten()
    h_b = pd.read_excel(filepath, usecols = "AN", skiprows = 0).to_numpy().flatten()
    h_a = pd.read_excel(filepath, usecols = "BL", skiprows = 0).to_numpy().flatten()

    #errors

    o_iii_5007_err_up = pd.read_excel(filepath, usecols = "AW", skiprows = 0).to_numpy().flatten()
    n_ii_6584_err_up = pd.read_excel(filepath, usecols = "BQ", skiprows = 0).to_numpy().flatten()
    s_ii_6717_err_up = pd.read_excel(filepath, usecols = "BU", skiprows = 0).to_numpy().flatten()
    s_ii_6731_err_up = pd.read_excel(filepath, usecols = "BY", skiprows = 0).to_numpy().flatten()
    o_i_6300_err_up = pd.read_excel(filepath, usecols = "BE", skiprows = 0).to_numpy().flatten()
    h_b_err_up = pd.read_excel(filepath, usecols = "AO", skiprows = 0).to_numpy().flatten()
    h_a_err_up = pd.read_excel(filepath, usecols = "BM", skiprows = 0).to_numpy().flatten()
    
    o_iii_5007_err_down = pd.read_excel(filepath, usecols = "AX", skiprows = 0).to_numpy().flatten()
    n_ii_6584_err_down = pd.read_excel(filepath, usecols = "BR", skiprows = 0).to_numpy().flatten()
    s_ii_6717_err_down = pd.read_excel(filepath, usecols = "BV", skiprows = 0).to_numpy().flatten()
    s_ii_6731_err_down = pd.read_excel(filepath, usecols = "BZ", skiprows = 0).to_numpy().flatten()
    o_i_6300_err_down = pd.read_excel(filepath, usecols = "BF", skiprows = 0).to_numpy().flatten()
    h_b_err_down = pd.read_excel(filepath, usecols = "AP", skiprows = 0).to_numpy().flatten()
    h_a_err_down = pd.read_excel(filepath, usecols = "BN", skiprows = 0).to_numpy().flatten()

    #average errors

    o_iii_5007_err = (o_iii_5007_err_down + o_iii_5007_err_up) / 2
    n_ii_6584_err = (n_ii_6584_err_down + n_ii_6584_err_up) / 2
    s_ii_6717_err = (s_ii_6717_err_down + s_ii_6717_err_up) / 2
    s_ii_6731_err = (s_ii_6731_err_down + s_ii_6731_err_up) / 2
    o_i_6300_err = (o_i_6300_err_down + o_i_6300_err_up) / 2
    h_b_err = (h_b_err_down + h_b_err_up) / 2
    h_a_err = (h_a_err_down + h_a_err_up) / 2
    

    #add sulphur doublet line intensities together to get combined intensity

    s_ii_6717_31 = s_ii_6717 + s_ii_6731
    s_ii_6717_31_err = np.sqrt(s_ii_6731_err**2 + s_ii_6717_err**2)
    
    #Get axis data for the BPT diagrams
    #Top left
    nii_ha = np.log10(n_ii_6584/h_a)
    nii_ha_err = np.sqrt((n_ii_6584_err/n_ii_6584) **2 + (h_a_err/h_a)**2) / np.log(10)
    
    #Top right
    sii_ha = np.log10(s_ii_6717_31/h_a)
    sii_ha_err = np.sqrt((s_ii_6717_31_err/s_ii_6717_31) **2 + (h_a_err/h_a)**2) / np.log(10)

    #Bottom
    oi_ha = np.log10(o_i_6300/h_a)
    oi_ha_err = np.sqrt((o_i_6300_err/o_i_6300) **2 + (h_a_err/h_a)**2) / np.log(10)
    
    #y-axis
    oiii_hb = np.log10(o_iii_5007/h_b)
    oiii_hb_err = np.sqrt((o_iii_5007_err/o_iii_5007) **2 + (h_b_err/h_b)**2) / np.log(10)

    
    x_kauff = np.linspace(-3, 0, 1000)
    y_kauff = n2kauffmann(x_kauff)

    x_kewley = np.linspace(-3, 0.2, 1000)
    y_kewleyn2 = n2kewley(x_kewley)
    y_kewleys2 = s2kewley(x_kewley)
    y_kewleyo1 = o1kewley(x_kewley)

    #plot
    #NII BPT diagram
    plt.plot(x_kauff, y_kauff, linestyle = "--", c = "k", label = "Kauffman 2003")
    plt.plot(x_kewley, y_kewleyn2, linestyle = "-", c = "k", label = "Kewley 2001")
    plt.errorbar(nii_ha, oiii_hb, yerr = oiii_hb_err, xerr = nii_ha_err, fmt='none', ecolor= "r")
    plt.xlabel("log([NII]6584/Halpha)")
    plt.ylabel("log([OIII]5007/Hbeta)")
    plt.text(-2, 0, "Starbust")
    plt.text(-0.4, -0.2, "Composite")
    plt.text(0.5, 0.8, "AGN")
    plt.xlim(-3, 1)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [NII]")
    plt.legend()
    plt.savefig("BPT_NII.png")
    plt.show()

    #SII BPT diagram
    plt.plot(x_kewley, y_kewleys2, linestyle = "-", c = "k", label = "Kewley 2001")
    plt.errorbar(sii_ha, oiii_hb, yerr = oiii_hb_err, xerr = sii_ha_err, fmt='none', ecolor= "g")
    plt.xlabel("log([SII]6717,31/Halpha)")
    plt.ylabel("log([OIII]5007/Hbeta)")
    plt.text(-2.5, -0.5, "Starburst")
    plt.text(0.3, -0.5, "LI(N)ER")
    plt.text(-0.2, 0.9, "Seyfert")
    plt.text
    plt.xlim(-3, 1)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [SII]")
    plt.legend()
    plt.savefig("BPT_SII.png")
    plt.show()

    #OI BPT diagram
    plt.plot(x_kewley, y_kewleyo1, linestyle = "-", c = "k", label = "Kewley 2001")
    plt.errorbar(oi_ha, oiii_hb, yerr = oiii_hb_err, xerr = oi_ha_err, fmt='none', ecolor= "b")
    plt.xlabel("log([OI]6300}/Halpha)")
    plt.ylabel("log([OIII]5007/Hbeta)")
    plt.text(-2.5, -0.5, "Starburst")
    plt.text(-1, -0.1, "LI(N)ER")
    plt.text(-1.5, 0.74, "Seyfert")
    plt.xlim(-3, -0.7)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [OI]")
    plt.legend()
    plt.savefig("BPT_OI.png")
    plt.show()

def main():
    extract_and_plot()
    
 
main()

