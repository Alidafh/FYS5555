import numpy as np
import matplotlib.pyplot as plt

def readfile(filename, skip):
    # input: "filename.txt", first line in file must be titles
    data = np.loadtxt("{}".format(filename), skiprows = skip)
    C = data[:,0]; M = data[:,-1]
    return C, M

c, M_A = readfile("datafiles/res_diff_A.txt", 0)
c, M_Z = readfile("datafiles/res_diff_Z.txt", 0)
c, M_H = readfile("datafiles/res_diff_H.txt", 0)
c, M_intf = readfile("datafiles/res_diff_AZ.txt", 0)
c, M_tot = readfile("datafiles/res_diff_tot.txt", 0)

cos, comp_A = readfile("datafiles/diff_A.txt", 3)
cos, comp_Z = readfile("datafiles/diff_Z.txt", 3)
cos, comp_H = readfile("datafiles/diff_H.txt", 3)
cos, comp_AZ = readfile("datafiles/diff_AZ.txt", 3)
cos, comp_tot = readfile("datafiles/diff_fi.txt", 3)

legend1 = [r"$d\sigma_{\gamma}$", r"$d\sigma_{Z}$", r"$d\sigma_{H}$",r"$d\sigma_{\gamma Z}$",r"$d\sigma_{fi}$"]

plt.figure(figsize=(10,5))
plt.title(r"Differential cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$ at $\sqrt{s} = 150 GeV$")
lines=plt.plot(c, M_A, "--", c, M_Z, "--",c, M_H,"--", c, M_intf,"--", c, M_tot, "k")
plt.legend(lines,legend1)
plt.xlabel(r"$\cos \theta$")
plt.ylabel(r"$d\sigma/d(\cos\theta)\quad $[pb/rad]")
plt.grid()
plt.savefig("figures/total_cross_all.pdf")
plt.show()

legend2 = [r"$d\sigma_{\gamma}$", r"$d\sigma_{Z}$",r"$d\sigma_{\gamma Z}$", r"$d\sigma_{fi}$"]

plt.figure(figsize=(10,5))
plt.title(r"Differential cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$ at $\sqrt{s} = 150 GeV$")
lines=plt.plot(c, M_A, "--", c, M_Z, "--", c, M_intf, "--", c, M_tot )
plt.legend(lines,legend2)
plt.xlabel(r"$\cos \theta$")
plt.ylabel(r"$d\sigma/d(\cos\theta)\quad $[pb/rad]")
plt.grid()
plt.savefig("figures/diff_A_Z_tot.pdf")
plt.show()
