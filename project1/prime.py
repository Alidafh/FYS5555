import numpy as np
import matplotlib.pyplot as plt

def readfile(filename, skip):
    # input: "filename.txt", first line in file must be titles
    data = np.loadtxt("datafiles/{}".format(filename), skiprows = skip)
    x = data[:,0]; y = data[:,-1]
    return x, y

cos, diff = readfile("prime_diff.txt", 3)
CM, total = readfile("prime_total.txt", 3)
CM2, A = readfile("prime_asym.txt", 3)


plt.figure(figsize=(10,5))
plt.title(r"Differential cross section for $\mu^- \mu^+ \rightarrow Z^{'} \rightarrow b \overline{b}$")
plt.plot(cos, diff)
plt.xlabel(r"$\cos \theta$")
plt.ylabel(r"$d\sigma/d\cos\theta\quad$[pb/rad]")
plt.grid()
plt.savefig("figures/diff_prime.pdf")
plt.show()

plt.figure(figsize=(10,5))
plt.title(r"Total cross section for $\mu^- \mu^+ \rightarrow Z^{'} \rightarrow b \overline{b}$")
plt.semilogy(CM, total)
plt.xlabel(r"$\sqrt{s}$")
plt.ylabel(r"$\sigma\quad$[pb]")
plt.grid()
plt.savefig("figures/total_prime.pdf")
plt.show()

plt.figure(figsize=(10,5))
plt.title(r"Asymmetry for $\mu^- \mu^+ \rightarrow Z^{'} \rightarrow b \overline{b}$")
plt.plot(CM2, A)
plt.xlabel(r"$\sqrt{s}$")
plt.ylabel(r"$A_{FB}$")
plt.grid()
plt.savefig("figures/asym_prime.pdf")
plt.show()
