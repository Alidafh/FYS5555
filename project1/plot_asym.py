import numpy as np
import matplotlib.pyplot as plt

def readfile(filename, skip):
    # input: "filename.txt", first line in file must be titles
    data = np.loadtxt("{}".format(filename), skiprows = skip)
    CM = data[:,0]; A = data[:,-1]
    return CM, A


CM_b, A_b = readfile("datafiles/w_A_bb.txt", 0)
CM_c, A_c = readfile("datafiles/w_A_cc.txt", 0)
CM_e, A_e = readfile("datafiles/w_A_ee.txt", 0)
CM_no, A_no = readfile("datafiles/asym_NO_AZ.txt", 0)
"""
for i in range(len(CM_b)):
    if A_b[i] == A_no[i]:
        print(i, CM_b[i], A_b[i])
    elif A_b[i] < A_no[i]:
        print("smaller", i)
    elif A_b[i] > A_no[i]:
        print("LARGER")
"""
print (CM_b[85], CM_no[85])

CCM_b, cA_b = readfile("datafiles/asym_total.txt", 3)
CCM_c, cA_c = readfile("datafiles/asym_CC.txt", 3)
CCM_e, cA_e = readfile("datafiles/asym_EE.txt", 3)
"""
legends = ["CompHEP", r"$\mu^- \mu^+ \rightarrow b \overline{b}$", r"$\mu^- \mu^+ \rightarrow c \overline{c}$", r"$\mu^- \mu^+ \rightarrow e^+ e^-$"]
legends2 = [r"CompHEP"]
plt.figure(figsize=(10,5))
plt.title(r"Asymmetry comparison for $\mu^+ \mu^- \rightarrow b\overline{b}, c\overline{c}, e^+ e^-$")
line = plt.plot(CCM_b,cA_b, "k+", CCM_c,cA_c, "k+", CCM_e,cA_e, "k+", CM_b, A_b, CM_c, A_c, CM_e, A_e)
plt.legend(line[2:],legends)
plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
plt.ylabel(r"$A_{FB}$")
plt.grid()
plt.savefig("figures/asym_comparison.pdf")
plt.show()
"""

legends = [r"$A(\sigma_{fi})$", r"$A\sigma_{\gamma+Z+H}$" ]
plt.figure(figsize=(10,5))
plt.title(r"Asymmetry for $\mu^+ \mu^- \rightarrow b \overline{b}$")
line = plt.plot(CM_b, A_b,"r", CM_no, A_no,"b")
plt.legend(line,legends)
plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
plt.ylabel(r"$A_{FB}$")
plt.grid()
plt.savefig("figures/asym_no_AZ.pdf")
plt.show()
