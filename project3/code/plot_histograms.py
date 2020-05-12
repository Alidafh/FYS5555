import ROOT as ro
import sys, os
import re
from run_analysis import get_filenames

ro.gStyle.SetOptFit(1111)          # ROOT being told to show all fitting parameters in box!

def get_hist(file, name):
    infile = ro.TFile(file)
    hist = ro.TH1F()
    hist = infile.Get(name).Clone("new_"+name)
    hist.SetDirectory(0)
    infile.Close()
    return hist

def make_dict(path, filenames):
    name_list = [re.match("outfile.(.*?).root", file).group(1) for file in filenames]
    hist_all_tmp = {}
    hist_unc_tmp = {}
    for name, file in zip(name_list,filenames):
        hist_all_tmp[name] = get_hist(path+file, "hist_mass_all")
        hist_unc_tmp[name] = get_hist(path+file, "hist_mass_unconv")
    h1 = ro.TH1F("a1", "a1", 30,105,160)
    h2 = ro.TH1F("a2", "a2", 30, 105, 160)
    for k1, k2 in zip(hist_all_tmp, hist_unc_tmp):
        h1.Add(hist_all_tmp[k1])
        h2.Add(hist_unc_tmp[k2])
    hist_all_tmp["combined"] = h1.Clone("hist_all_combined")
    hist_unc_tmp["combined"] = h2.Clone("hist_unc_combined")
    return hist_all_tmp, hist_unc_tmp

hist_names = ["hist_mass_all", "hist_mass_unconv"]
path = "/home/alida/Documents/uio/Master/FYS5555/project3/code/output/"
d_path = path+"data/"
m_path = path+"mc/"

data_filenames = get_filenames(d_path)
mc_filenames = get_filenames(m_path)

dict_data, dict_data_unc = make_dict(d_path, data_filenames)
dict_mc, dict_mc_unc = make_dict(m_path, mc_filenames)


hist_data = dict_data.get("combined").Clone("data_all")
hist_mc = dict_mc.get("combined").Clone("mc_all")

# signal fit
sig_fit = ro.TF1("sig", "gaus")
hist_mc.Clone("fit_all_mc").Fit("sig", "Q0", "", 120,130)
par_sig = [sig_fit.GetParameters()[i] for i in range(3)]


#signal+background fit
sb = ro.TF1("s+b", "([0]+[1]*x+[2]*x^2+[3]*x^3)+[4]*exp(-0.5*((x-[5])/[6])^2)", 105, 160);
sb.SetLineColor(2)
sb.SetLineStyle(1)
hist_data.Clone("fit_all_data_sb").Fit("s+b", "Q0")
sb.FixParameter(5,125.0);   #always fixed to 125 GeV,  TODO: find out why
sb.FixParameter(4,par_sig[1]);
sb.FixParameter(6,par_sig[2]);
par_sb = [sb.GetParameters()[i] for i in range(6)]

#background fit
bkg_fit = ro.TF1("bkg", "pol3")
bkg_fit.SetLineColor(4)
bkg_fit.SetLineStyle(9)
hist_data.Clone("fit_all_data").Fit("bkg", "Q0","",105,160)
[bkg_fit.FixParameter(i,par_sb[i]) for i in range(3)]

c1 = ro.TCanvas("c1", "c1", 1000, 600)
c1.cd()

hist_data.GetXaxis().SetTitle("m_{#gamma#gamma} [GeV]")
hist_data.GetYaxis().SetTitle("Events/GeV")
#hist_data.SetMarkerStyle(9)
hist_data1 = hist_data.Clone("new")
hist_data1.Draw("P*")
hist_data1.Fit("bkg", "Q","", 105,160)
hist_data.Draw("P*same")
hist_data.Fit("s+b","","", 105,160)


c1.Update()
c1.Draw()

"""
#pad2.Draw()
#pad2.cd()
#hist_data.Fit("bkg")
#pad1 = ro.TPad("pad1","",0,0,1,1)
#pad2 = ro.TPad("pad2","",0,0,1,1)
#pad2.SetFillStyle(4000) #will be transparent
#pad2.SetFrameFillStyle(0)

#pad1.Draw()
#pad1.cd()
c1 = ro.TCanvas("c1", "c1", 1000, 400)
hist_all_data = add(dict_hist)
hist_all_data.Draw("P*")

hist_unc_data = add(dict_hist_unc)
hist_unc_data.Draw("P*SAME")
c1.Draw()
"""





#name_list = [re.match("outfile.(.*?).root", file).group(1) for file in filenames]
#data = []
#mc = []
#for file in filenames:
#    a = re.match("outfile.(.*?).root", file).group(1)
#    if a.split("_")[0]=="data": data.append(file)
#    if a.split("_")[0]=="mc": mc.append(file)
