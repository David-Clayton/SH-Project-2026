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

def main():
    """Extract BPT data for the CLASSY and LzLCS samples, and
    plot them together."""

    filepathclassy = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\BPT Diagrams\CLASSYBPTdata.csv"
    filepathlzlcs = r"C:\Users\drcla\OneDrive\Senior Honours Project\Joint Diagrams\BPT Diagrams\LzLCSBPTdata.csv"

    #CLASSY
    classy_nii = pd.read_csv(filepathclassy, delimiter = ",", usecols=[0], header = 0).to_numpy().flatten()
    classy_nii_err = pd.read_csv(filepathclassy, delimiter = ",", usecols=[1], header = 0).to_numpy().flatten()
    classy_sii = pd.read_csv(filepathclassy, delimiter = ",", usecols=[2], header = 0).to_numpy().flatten()
    classy_sii_err = pd.read_csv(filepathclassy, delimiter = ",", usecols=[3], header = 0).to_numpy().flatten()
    classy_oi = pd.read_csv(filepathclassy, delimiter = ",", usecols=[4], header = 0).to_numpy().flatten()
    classy_oi_err = pd.read_csv(filepathclassy, delimiter = ",", usecols=[5], header = 0).to_numpy().flatten()
    classy_oiii = pd.read_csv(filepathclassy, delimiter = ",", usecols=[6], header = 0).to_numpy().flatten()
    classy_oiii_err = pd.read_csv(filepathclassy, delimiter = ",", usecols=[7], header = 0).to_numpy().flatten()

    #LzLCS

    lzlcs_nii = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[0], header = 0).to_numpy().flatten()
    lzlcs_nii_err = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[1], header = 0).to_numpy().flatten()
    lzlcs_sii = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[2], header = 0).to_numpy().flatten()
    lzlcs_sii_err = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[3], header = 0).to_numpy().flatten()
    lzlcs_oi = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[4], header = 0).to_numpy().flatten()
    lzlcs_oi_err = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[5], header = 0).to_numpy().flatten()
    lzlcs_oiii = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[6], header = 0).to_numpy().flatten()
    lzlcs_oiii_err = pd.read_csv(filepathlzlcs, delimiter = ",", usecols=[7], header = 0).to_numpy().flatten()

    #Functions
    x_kauff = np.linspace(-3, 0, 1000)
    y_kauff = n2kauffmann(x_kauff)

    x_kewley = np.linspace(-3, 0.2, 1000)
    y_kewleyn2 = n2kewley(x_kewley)
    y_kewleys2 = s2kewley(x_kewley)
    y_kewleyo1 = o1kewley(x_kewley)

    #Joint NII BPT diagram
    plt.plot(x_kauff, y_kauff, linestyle = "--", c = "k", label = "Kauffmann 2003")
    plt.plot(x_kewley, y_kewleyn2, linestyle = "-", c = "k", label = "Kewley 2001")
    plt.errorbar(classy_nii, classy_oiii, yerr = classy_oiii_err, xerr = classy_nii_err, fmt='none', ecolor= "slateblue", label = "CLASSY")
    plt.errorbar(lzlcs_nii, lzlcs_oiii, yerr = lzlcs_oiii_err, xerr = lzlcs_nii_err, fmt='none', ecolor= "salmon", label = "LzLCS")
    plt.xlabel(r"$log_{10}([NII]\lambda6584/H{\alpha})$", fontsize = 12)
    plt.ylabel(r"$log_{10}([OIII]\lambda5007/H{\beta})$", fontsize = 12)
    plt.text(-2, 0, "Starbust")
    plt.text(-0.4, -0.2, "Composite")
    plt.text(0.5, 0.8, "AGN")
    plt.xlim(-3, 1)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [NII]", fontsize = 16)
    plt.tight_layout()
    plt.legend()
    plt.savefig("BPT_NII.png")
    plt.show()

    #Joint SII BPT diagram
    plt.plot(x_kewley, y_kewleys2, linestyle = "-", c = "k", label = "Kewley 2001")
    plt.errorbar(classy_sii, classy_oiii, yerr = classy_oiii_err, xerr = classy_sii_err, fmt='none', ecolor= "slateblue", label = "CLASSY")
    plt.errorbar(lzlcs_sii, lzlcs_oiii, yerr = lzlcs_oiii_err, xerr = lzlcs_sii_err, fmt='none', ecolor= "salmon", label = "LzLCS")
    plt.xlabel(r"$log_{10}([SII]\lambda\lambda6717,31/H{\alpha})$", fontsize = 12)
    plt.ylabel(r"$log_{10}([OIII]\lambda5007/H{\beta})$", fontsize = 12)
    plt.text(-2.5, -0.5, "Starburst")
    plt.text(0.3, -0.5, "LI(N)ER")
    plt.text(-0.2, 0.9, "Seyfert")
    plt.text
    plt.xlim(-3, 1)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [SII]", fontsize = 16)
    plt.tight_layout()
    plt.legend()
    plt.savefig("BPT_SII.png")
    plt.show()

    #Joint OI BPT diagram
    plt.plot(x_kewley, y_kewleyo1, linestyle = "-", c = "k", label = "Kewley 2001")
    plt.errorbar(classy_oi, classy_oiii, yerr = classy_oiii_err, xerr = classy_oi_err, fmt='none', ecolor= "slateblue", label = "CLASSY")
    plt.errorbar(lzlcs_oi, lzlcs_oiii, yerr = lzlcs_oiii_err, xerr = lzlcs_oi_err, fmt='none', ecolor= "salmon", label = "LzLCS")
    plt.xlabel(r"$log_{10}([OI]\lambda6300/H{\alpha})$", fontsize = 12)
    plt.ylabel(r"$log_{10}([OIII]\lambda5007/H{\beta})$", fontsize = 12)
    plt.text(-2.5, -0.5, "Starburst")
    plt.text(-1, -0.1, "LI(N)ER")
    plt.text(-1.5, 0.74, "Seyfert")
    plt.xlim(-3, -0.7)
    plt.ylim(-1, 1)
    plt.title("BPT diagram for [OI]", fontsize = 16)
    plt.tight_layout()
    plt.legend()
    plt.savefig("BPT_OI.png")
    plt.show()

    
if __name__ == "__main__":
    main()