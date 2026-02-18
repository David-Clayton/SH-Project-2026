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


    #add sulphur doublet line intensities together to get combined intensity

    s_ii_6717_31 = s_ii_6717 + s_ii_6731
    s_ii_6717_31_err_up = np.sqrt(s_ii_6717_err_up **2 + s_ii_6731_err_up ** 2)
    s_ii_6717_31_err_down = np.sqrt(s_ii_6717_err_down **2 + s_ii_6731_err_down ** 2)
    

    #Get axis data 
    x_tl = np.log10(n_ii_6584/h_a)
    x_tl_err_up = x_tl * np.sqrt((n_ii_6584_err_up ** 2 / n_ii_6584 **2) + (h_a_err_up **2 / h_a **2 ))
    x_tl_err_down = x_tl * np.sqrt((n_ii_6584_err_down ** 2 / n_ii_6584 **2) + (h_a_err_down **2 / h_a **2 ))
    
    x_tr = np.log10(s_ii_6717_31/h_a)
    x_tr_err_up = x_tr * np.sqrt((s_ii_6717_31_err_up ** 2 / s_ii_6717_31 **2) + (h_a_err_up **2 / h_a **2 ))
    x_tr_err_down = x_tr * np.sqrt((s_ii_6717_31_err_down ** 2 / s_ii_6717_31 **2) + (h_a_err_down **2 / h_a **2 ))

    x_b = np.log10(o_i_6300/h_a)
    x_b_err_up = x_b * np.sqrt((o_i_6300_err_up ** 2 / o_i_6300 **2) + (h_a_err_up **2 / h_a **2 ))
    x_b_err_down = x_b * np.sqrt((o_i_6300_err_down ** 2 / o_i_6300 **2) + (h_a_err_down **2 / h_a **2 ))
    
    y = np.log10(o_iii_5007/h_b)
    y_err_up = y * np.sqrt((o_iii_5007_err_up ** 2 / o_iii_5007 **2) + (h_b_err_up **2 / h_b **2 ))
    y_err_down = y * np.sqrt((o_iii_5007_err_down ** 2 / o_iii_5007 **2) + (h_b_err_down **2 / h_b **2 ))

    x_kauff = np.linspace(-3, 0, 1000)
    y_kauff = n2kauffmann(x_kauff)

    x_kewley = np.linspace(-3, 0.2, 1000)
    y_kewleyn2 = n2kewley(x_kewley)
    y_kewleys2 = s2kewley(x_kewley)
    y_kewleyo1 = o1kewley(x_kewley)

    #plot
    
    plt.scatter(x_tl, y, s = 4, c = "r")
    plt.plot(x_kauff, y_kauff, linestyle = "--", c = "k", label = "Kauffman 2003")
    plt.plot(x_kewley, y_kewleyn2, linestyle = "-", c = "k", label = "Kewley 2001")
    #plt.errorbar(x_tl, y, yerr = [y_err_down / (np.log(10) * y), y_err_up  / (np.log(10) * y)], xerr = [x_tl_err_down / (np.log(10)*x_tl), x_tl_err_up /(np.log(10)*x_tl)], fmt='none', ecolor= "r")
    plt.xlabel("log([NII]6584/Halpha)")
    plt.ylabel("log([OIII]5007/Hbeta)")
    plt.xlim(-3, 1)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [NII]")
    plt.legend()
    plt.savefig("BPT_NII.png")
    plt.show()


    plt.scatter(x_tr, y, s = 4, c = "g")
    plt.plot(x_kewley, y_kewleys2, linestyle = "-", c = "k", label = "Kewley 2001")
    #plt.errorbar(x_tr, y, yerr = [y_err_down / (np.log(10) * y), y_err_up  / (np.log(10) * y)], xerr = [x_tr_err_down / (np.log(10)*x_tr), x_tr_err_up /(np.log(10)*x_tr)], fmt='none', ecolor= "g")
    
    plt.xlabel("log([SII]6717,31/Halpha)")
    plt.ylabel("log([OIII]5007/Hbeta)")
    plt.xlim(-3, 1)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [SII]")
    plt.legend()
    plt.savefig("BPT_SII.png")
    plt.show()

    plt.scatter(x_b, y, s = 4, c = "b")
    plt.plot(x_kewley, y_kewleyo1, linestyle = "-", c = "k", label = "Kewley 2001")
    #plt.errorbar(x_b, y, yerr = [y_err_down / (np.log(10) * y), y_err_up  / (np.log(10) * y)], xerr = [x_b_err_down / (np.log(10)*x_b), x_b_err_up /(np.log(10)*x_b)], fmt='none', ecolor= "b")
    plt.xlabel("log([NII]6584/Halpha)")
    plt.ylabel("log([OIII]5007/Hbeta)")
    plt.xlim(-3, -0.7)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [OI]")
    plt.legend()
    plt.savefig("BPT_OI.png")
    plt.show()
    

    

def main():
    extract_and_plot()
    
 
main()

