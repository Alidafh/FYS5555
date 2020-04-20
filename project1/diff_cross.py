import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

"""
Constants, masses in GeV
"""
mu = 0.10566
mb = 4.18
#mb = 1.275       #mass of c
#mb = 0.00051099    # mass of e
mz = 91.1876
mw = 80.379
mh = 125.18


G_F = 1.1663787e-5
sin2_w = 0.2315
cos_w = np.sqrt(1 - sin2_w)
g_w = np.sqrt(8*G_F*mw**2/np.sqrt(2))
g_z = g_w/cos_w
e = g_w*np.sqrt(sin2_w)
wz = 2.4952    #width of z
wh = 4.07e-3

Cv = -0.04
Ca = -0.5
Cvb = -0.35
Cab = -0.5
#Cvb = 0.19  # for c
#Cab = 0.5   # for c
#Cvb = -0.04 # for e
#Cab = -0.5  # for e


f1 = (Cv**2 + Ca**2)*(Cvb**2 + Cab**2) + 4*Cv*Ca*Cvb*Cab
f2 = (Cv**2 + Ca**2)*(Cvb**2 + Cab**2) - 4*Cv*Ca*Cvb*Cab
f3 = (Cv**2 + Ca**2)*(Cvb**2 - Cab**2)
f4 = (Cv**2 - Ca**2)*(Cvb**2 + Cab**2)
f5 = (Cv**2 - Ca**2)*(Cvb**2 - Cab**2)

g1 = (Cv*Cvb + Ca*Cab)
g2 = (Cv*Cvb - Ca*Cab)
g3 = (Cv*Cvb)

j = 200
c = np.linspace(-1, 1, j)

"""
Functions
"""

def readfile(filename):
    # input: "filename.txt", first line in file must be titles
    data = np.loadtxt("{}".format(filename), skiprows = 3)
    return data

def diff_cross(s, p12, p13, p14, p23, p24, p34):
    """
    Returns differential cross sections for :
        0-QED, 1-NC, 2-Higgs, 3-Interference Z and QED, 4-total
    pij - product of 4-momentum (pi*pj)
    """
    const = (3*1/(2.56810e-9*32*np.pi*s))* (np.sqrt((s - 4*mb**2)/(s - 4*mu**2)))
#    const = (1/(2.56810e-9*32*np.pi*s))* (np.sqrt(abs((s - 4*mb**2)/(s - 4*mu**2))))    #for EE
    alpha = (8*e**4)/(3*s)**2
    #alpha = (4*8*e**4)/(3*s)**2   #for CC
    #alpha = (8*e**4)/(s**2) # for EE
    beta = g_z**4/(2*((s-mz**2)**2 + (mz*wz)**2))
    kappa = (g_w**4 * mu**2 * mb**2)/(4*mw**4 *((s-mh**2)**2 + (mh*wh)**2))
    phi = np.real((2*e*g_z)**2/(3*s*(s - mz**2 - 1j*mz*wz)))
    #phi = np.real((2*e*g_z)**2/(s*(s - mz**2 + 1j*mz*wz))) #for EE
    #phi = np.real((-2*(2*e*g_z)**2)/(3*s*(s - mz**2 + 1j*mz*wz)))   #for cc
    M_qed = const*alpha*(p14*p23 + p13*p24 + p12*mb**2 + p34*mu**2 + 2*(mb*mu)**2)
    M_nc = const*beta*(p14*p23*f1 + p13*p24*f2 + p12*f3*mb**2 + p34*f4*mu**2 + 2*f5*(mb*mu)**2)
    M_h = const*kappa*(p12*p34 - p12*mb**2 - p34*mu**2 + (mu*mb)**2)
    M_intf = const*phi*(p14*p23*g1 + p13*p24*g2 + g3*(p12*mb**2 + p34*mu**2 + 2*(mb*mu)**2))
    M_fi = M_qed + M_nc + M_h + M_intf
    #M_fi = M_qed + M_nc + M_intf    #for EE
    #M_fi = M_qed + M_h    #to see what happens
    return M_qed, M_nc, M_h, M_intf, M_fi

def kinematics(CM_energy):
    E_cm = CM_energy
    s = E_cm**2
    E = 0.5*E_cm
    p = np.sqrt(E**2 - mu**2)
    k = np.sqrt(E**2 - mb**2)
    p12 = (E**2 + p**2)*np.ones(len(c))
    p13 = E**2 - p*k*c
    p14 = E**2 + p*k*c
    p23 = p14
    p24 = p13
    p34 = (E**2 + k**2)* np.ones(len(c))
    return s, p12, p13, p14, p23, p24, p34

def plot_diff(M, comp_file, legend1, legend2):
    filename = "datafiles/{}".format(comp_file)
    #print ("{}".format((comp_file).split(".")[0]))
    comp = readfile(filename)
    legend = [legend1, legend2]
    plt.figure(figsize=(7,3))
    plt.title(r"Differential cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$ at $\sqrt{s} = 150 GeV$")
    plt.plot(comp[:,0], comp[:,1], "k+", c, M,)
    plt.legend([legend2, legend1])
    plt.xlabel(r"$\cos \theta$")
    plt.ylabel(r"$d\sigma/d(\cos\theta)\quad $[pb/rad]")
    plt.grid()
    plt.savefig("figures/{}.pdf".format((comp_file).split(".")[0]))
    plt.show()

def plot_total(sigma, CM_enrg, comp_file, legend1, legend2):
    filename = "datafiles/{}".format(comp_file)
    comp = readfile(filename)
    legend = [legend1, legend2]
    plt.figure(figsize=(7,3))
    plt.title(r"Total cross section for $\mu^- \mu^+ \rightarrow b \overline{b}$")
    #plt.semilogy(CM_enrg, sigma, comp[:,0], comp[:,1], "k+")
    plt.plot(CM_enrg, sigma, comp[:,0], comp[:,1], "k+")
    plt.legend([legend1, legend2])
    plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
    plt.ylabel(r"$\sigma\quad$[pb]")
    plt.grid()
    plt.savefig("figures/{}.pdf".format((comp_file).split(".")[0]))
    plt.show()


def total_cross(number):
    #number: 0-qed, 1-nc, 2-h, 3-interference 4-total
    total = np.zeros(j)
    CM_enrg = np.linspace(10, 200, j)
    letters = ["A","Z","H","AZ","fi"]
    file = "total_{}.txt".format(letters[number])
    for i in range(j):
        s, p12, p13, p14, p23, p24, p34 = kinematics(CM_enrg[i])
        M = diff_cross(s, p12, p13, p14, p23, p24, p34)
        element = M[number]
        total[i] = integrate.simps(element, c)
    legend = [r"$\sigma_{\gamma}$", r"$\sigma_Z$", r"$\sigma_H$", r"$\sigma_{{\gamma Z}}$", r"$\sigma_{fi}$"]
    plot_total(total, CM_enrg, file, legend[number], "CompHEP")
#    return total, CM_enrg

def Asymmetry(number):
    #number: 0-qed, 1-nc, 2-h, 3-interference 4-total
    F = np.zeros(j)
    B = np.zeros(j)
    A = np.zeros(j)
    CM_enrg = np.linspace(10, 200, j)
    c1 = np.linspace(0, -1, j)
    c2 = np.linspace(1, 0, j)
    for i in range(j):
        s, p12, p13, p14, p23, p24, p34 = kinematics(CM_enrg[i])
        M = diff_cross(s, p12, p13, p14, p23, p24, p34)
        element = M[number]
        B[i] = integrate.simps(element[:100])
        F[i] = integrate.simps(element[100:])
        A[i] = (F[i] - B[i])/(F[i] + B[i])
#    legend = [r"$\sigma_{\gamma}$", r"$\sigma_Z$", r"$\sigma_H$", r"$\sigma_{{\gamma Z}}$", r"$\sigma_{fi}$"]
    return A, CM_enrg

def differential():
    #Differential cross section for ecm=150GeV
    CM_energy = 150
    s, p12, p13, p14, p23, p24, p34 = kinematics(CM_energy)
    M_qed, M_nc, M_h, M_intf, M_fi = diff_cross(s, p12, p13, p14, p23, p24, p34)
    plot_diff(M_qed, "diff_A.txt", r"$\langle|\mathcal{M}_{\gamma}|^2 \rangle$", "CompHEP")
    plot_diff(M_nc, "diff_Z.txt", r"$\langle|\mathcal{M}_{Z}|^2 \rangle$", "CompHEP")
    plot_diff(M_h, "diff_H.txt", r"$\langle|\mathcal{M}_{H}|^2 \rangle$", "CompHEP")
    plot_diff(M_intf, "diff_AZ.txt", r"$\mathcal{X}_{\gamma Z}$", "CompHEP")
    plot_diff(M_fi, "diff_fi.txt", r"$\langle|\mathcal{M}_{fi}|^2 \rangle$", "CompHEP")
    return M_qed, M_nc, M_h, M_intf, M_fi

def total():
    total_cross(0); total_cross(1); total_cross(2); total_cross(3); total_cross(4)

def write(CM, A, name):
    f = open("datafiles/{}.txt".format(name), "w")
    for i in range(j):
        line = "{}  {}\n".format(CM[i], A[i])
        f.write(line)
    f.close()

def writediff(c, M, name):
    f = open("datafiles/res_{}.txt".format(name), "w")
    for i in range(j):
        line = "{}  {}\n".format(c[i], M[i])
        f.write(line)
    f.close()

def writetotal(cm, sigma, name):
    f = open("datafiles/w_tot_{}.txt".format(name), "w")
    for i in range(j):
        line = "{}  {}\n".format(cm[i], sigma[i])
        f.write(line)
    f.close()
"""
tA, cm = total_cross(0)
tZ, cm= total_cross(1)
tH, cm = total_cross(2)
tintf, cm = total_cross(3)
tfi, cm = total_cross(4)

writetotal(cm, tA, "tot_A")
writetotal(cm, tZ, "tot_Z")
writetotal(cm, tH, "tot_H")
writetotal(cm, tintf, "tot_AZ")
writetotal(cm, tfi, "tot_fi")
"""

"""
M_qed, M_nc, M_h, M_intf, M_fi = differential()

writediff(c, M_qed, "diff_A")
writediff(c, M_nc, "diff_Z")
writediff(c, M_h, "diff_H")
writediff(c, M_intf, "diff_AZ")
writediff(c, M_fi, "diff_tot")
"""
differential()
#total()
"""
comphep = readfile("datafiles/asym_A.txt")
comphepA = readfile("datafiles/asym_total.txt")

A_A, CM_A = Asymmetry(0)
A_Z, CM_Z = Asymmetry(1)
A_H, CM_H = Asymmetry(2)
A_AZ, CM_AZ = Asymmetry(3)
A_tot, CM_tot = Asymmetry(4)

#write(CM_tot, A_tot, "asym_NO_AZ")
#comphep = readfile("datafiles/asym_AZ3.txt")
"""
"""
legends = ["A", "Comp"]
plt.plot(CM_AZ, A_AZ, comphep[:,0], comphep[:,-1])
plt.legend(legends)
plt.show()
"""

"""
legends = [r"$A(\sigma_{\gamma})$", "$A(\sigma_{fi})$" ]
plt.figure(figsize=(10,5))
plt.title(r"Asymmetry for $\mu^+ \mu^- \rightarrow b \overline{b}$")
plt.plot(CM_A, A_A, "r", CM_tot, A_tot, "b")
plt.legend(legends)
plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
plt.ylabel(r"$A_{FB}$")
plt.grid()
#plt.savefig("figures/asym_bb_A_tot.pdf")
#plt.show()
"""
"""
legends = [r"$A(\sigma_{\gamma})$", "$A(\sigma_{Z})$","$A(\sigma_{AZ})$","$A(\sigma_{fi})$" ]
plt.figure(figsize=(10,5))
plt.title(r"Asymmetry for $\mu^+ \mu^- \rightarrow b \overline{b}$")
plt.plot(CM_A, A_A, CM_Z, A_Z, CM_H, A_H , CM_AZ, A_AZ,CM_A, A_tot)
#plt.legend(legends)
plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
plt.ylabel(r"$A_{FB}$")
plt.grid()
#plt.savefig("figures/asym_bb_total.pdf")
plt.show()
"""
"""
legends = ["CompHEP", r"$A(\sigma_{\gamma})$", r"$A(\sigma_{fi})$" ]
plt.figure(figsize=(10,5))
plt.title(r"Asymmetry for $\mu^+ \mu^- \rightarrow b \overline{b}$")
line = plt.plot(comphep[:,0], comphep[:,-1], "k+", comphepA[:,0], comphepA[:,-1], "k+", CM_A, A_A,CM_A, A_tot)
plt.legend(line[1:],legends)
plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
plt.ylabel(r"$A_{FB}$")
plt.grid()
plt.savefig("figures/asym_bb_A_total.pdf")
plt.show()
"""
"""
legends = [r"$A(\sigma_{fi})$" ]
plt.figure(figsize=(10,5))
plt.title(r"Asymmetry for $\mu^+ \mu^- \rightarrow b \overline{b}$")
line = plt.plot(CM_tot, A_tot)
plt.legend(line,legends)
plt.xlabel(r"$\sqrt{s}\quad$[GeV]")
plt.ylabel(r"$A_{FB}$")
plt.grid()
plt.savefig("figures/asym_no_AZ.pdf")
plt.show()
"""
