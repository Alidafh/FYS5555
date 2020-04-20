import numpy as np
import matplotlib.pyplot as plt

def readfile(filename, skip):
    # input: "filename.txt", first line in file must be titles
    data = np.loadtxt("{}".format(filename), skiprows = skip)
    CM = data[:,0]; sigma = data[:,-1]
    return CM, sigma

c, tot_A = readfile("datafiles/w_tot_tot_A.txt", 0)
c, tot_Z = readfile("datafiles/w_tot_tot_Z.txt", 0)
c, tot_H = readfile("datafiles/w_tot_tot_H.txt", 0)
c, tot_AZ = readfile("datafiles/w_tot_tot_AZ.txt", 0)
c, tot = readfile("datafiles/w_tot_tot_fi.txt", 0)

ch, comp_A = readfile("datafiles/total_A.txt", 3)
ch, comp_Z = readfile("datafiles/total_Z.txt", 3)
ch, comp_H = readfile("datafiles/total_H.txt", 3)
ch, comp_AZ = readfile("datafiles/total_AZ.txt", 3)
ch, comp_tot = readfile("datafiles/total_fi.txt", 3)

legend1 = ["CompHEP", r"$\sigma_{\gamma}$", r"$\sigma_{Z}$", r"$\sigma_{H}$",r"$\sigma_{\gamma Z}$",r"$\sigma_{fi}$"]
leg = [r"$\sigma_{fi}$", r"$\sigma_{\gamma}$", r"$\sigma_Z$"]
leg2 = ["CompHEP", r"$\sigma_{\gamma}$"]
plt.figure(figsize=(10,5))
plt.title(r"Total cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$")
lines=plt.plot(ch, comp_A, "k+", c, tot_A)
plt.legend(lines,leg)
plt.xlabel(r"$\sqrt{s}$")
plt.ylabel(r"$\sigma\quad$ [pb]")
plt.grid()
#plt.savefig("figures/total_A_Z_tot.pdf")
plt.show()

"""
plt.figure(figsize=(10,5))
plt.title(r"Differential cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$ at $\sqrt{s} = 150 GeV$")
lines=plt.plot(ch, comp_A, "k+", ch, comp_Z, "k+", ch, comp_H,"k+",  ch, comp_AZ, "k+", ch, comp_tot, "k+", c, tot_A, c, tot_Z, c, tot_H, c, tot_AZ, c, tot)
plt.legend(lines[4:],legend1)
plt.xlabel(r"$\sqrt{s}$")
plt.ylabel(r"$\sigma\quad$ [pb]")
plt.grid()
#plt.savefig("figures/all_tot_cross.pdf")
plt.show()
"""

"""
legend2 = ["CompHEP", r"$d\sigma_{\gamma}$", r"$d\sigma_{Z}$", r"$d\sigma_{fi}$"]

plt.figure(figsize=(10,5))
plt.title(r"Differential cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$ at $\sqrt{s} = 150 GeV$")
lines=plt.plot(ch, comp_A, "k+", ch, comp_Z, "k+", ch, comp_tot, "k+", c, tot_A, c, tot_Z, c, tot)
plt.legend(lines[2:],legend2)
plt.xlabel(r"$\sqrt{s}$")
plt.ylabel(r"$\sigma\quad $[pb]")
plt.grid()
#plt.savefig("figures/diff_A_Z_tot.pdf")
plt.show()
"""
