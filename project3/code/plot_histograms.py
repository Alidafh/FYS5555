import ROOT as ro
import numpy as np
import sys, os
import re
from run_analysis import get_filenames

ro.gStyle.SetOptFit(1)
ro.gStyle.SetOptStat(0);
ro.gStyle.SetPadLeftMargin(0.13)
ro.gStyle.SetLegendBorderSize(0)
ro.gStyle.SetPalette(1)
ro.gStyle.SetGridStyle(2)
ro.gStyle.SetPadLeftMargin(0.13)
ro.TH1.AddDirectory(ro.kFALSE)
ro.gStyle.SetEndErrorSize(0.);
ro.gStyle.SetErrorX(0.0);
#ro.gROOT.SetBatch(1)

def get_hist(file, name):
    infile = ro.TFile(file)
    hist = ro.TH1F()
    hist = infile.Get(name).Clone("new_"+name)
    #hist.SetDirectory(0)
    infile.Close()
    return hist

def make_dict(path, filenames, title):
    name_list = [re.match("outfile.(.*?).root", file).group(1) for file in filenames]
    hist_all_tmp = {}
    hist_unc_tmp = {}
    for name, file in zip(name_list,filenames):
        hist_all_tmp[name] = get_hist(path+file, "hist_mass_all")
        hist_all_tmp[name].SetTitle(title)
        hist_unc_tmp[name] = get_hist(path+file, "hist_mass_unconv")
    h1 = ro.TH1F("a1", "a1", 30,105,160)
    h2 = ro.TH1F("a2", "a2", 30, 105, 160)
    for k1, k2 in zip(hist_all_tmp, hist_unc_tmp):
        h1.Add(hist_all_tmp[k1])
        h2.Add(hist_unc_tmp[k2])
    hist_all_tmp["combined"] = h1.Clone("hist_all_combined")
    hist_all_tmp["combined"].SetMarkerStyle(20)
    hist_all_tmp["combined"].SetTitle(title)
    hist_unc_tmp["combined"] = h2.Clone("hist_unc_combined")
    hist_unc_tmp["combined"].SetMarkerStyle(20)
    hist_unc_tmp["combined"].SetTitle(title)
    return hist_all_tmp, hist_unc_tmp

hist_names = ["hist_mass_all", "hist_mass_unconv"]
path = "/home/alida/Documents/uio/Master/FYS5555/project3/code/output/"
d_path = path+"data/"
m_path = path+"mc/"

data_filenames = get_filenames(d_path)
mc_filenames = get_filenames(m_path)

dict_data, dict_data_unc = make_dict(d_path, data_filenames, "Data; m_{#gamma#gamma};Events")
dict_mc, dict_mc_unc = make_dict(m_path, mc_filenames, "Monte Carlo; m_{#gamma#gamma};Events")

hist_data = dict_data.get("combined").Clone("fit data")
hist_mc = dict_mc.get("combined").Clone("fit mc")

#hist_data = dict_data_unc.get("combined").Clone("fit data")
#hist_mc = dict_mc_unc.get("combined").Clone("fit mc")
#######################################################################
#                        PLOTTING
#######################################################################

c = ro.TCanvas("fitting", "fitting", 1200, 600)
c.Divide(2,1)

c.cd(1)
hist_mc.Draw("E")
hist_mc.Fit("gaus", "qWW", "", 120, 130)    #Signal fit
gaus_par = [hist_mc.GetFunction("gaus").GetParameter(i) for i in range(3)]

c.cd(2)
#signal+background model
sb = ro.TF1("s+b", "([0]+[1]*x+[2]*x^2+[3]*x^3)+[4]*exp(-0.5*((x-[5])/[6])^2)", 105, 160);
sb.SetTitle("Signal+Background model"); sb.SetLineColor(2); sb.SetLineStyle(1)
sb.FixParameter(4, gaus_par[0]);
sb.FixParameter(5,125.0);
sb.FixParameter(6, gaus_par[2]);
hist_data.Draw("E")
hist_data.Fit(sb, "R same", "")
sb_par = [hist_data.GetFunction("s+b").GetParameter(i) for i in range(7)]

c.Update(); c.Draw();
c.Print("output/figures/combined_fitting.pdf]")
c.Close()


c1 = ro.TCanvas("All", "All", 1000, 1200);
c1.Divide(1,2)

c1.cd(1);
l1 = ro.TLegend(0.63,0.70,0.97,0.93)
# Background model created using the parameters from the previous fit.
bkg = ro.TF1("bkg", "([0]+[1]*x+[2]*x^2+[3]*x^3)", 105, 160);
bkg.SetTitle("Diphoton invariant mass; m_{#gamma#gamma}; Events")
bkg.SetLineStyle(7); bkg.SetLineColor(1)
bkg.SetParameter(0,sb_par[0])
bkg.SetParameter(1,sb_par[1])
bkg.SetParameter(2,sb_par[2])
bkg.SetParameter(3,sb_par[3])
hist_data.Draw("E")
bkg.Draw("L same")
l1.AddEntry(bkg, "Background")
l1.AddEntry(sb, "Signal+background")
l1.AddEntry(hist_data, "Data")
l1.Draw()
c1.Update()

c1.cd(2)
l2 = ro.TLegend(0.6,0.6,0.88,0.88)

hist_nBkg = dict_data.get("combined").Clone("event-bkg")
hist_nBkg.SetTitle("Data - background; m_{#gamma#gamma}; Events - bkg ")
hist_nBkg.Add(bkg, -1)
hist_nBkg.Draw("E same")

sb_func = hist_data.GetFunction("s+b")
hist_sb = sb_func.CreateHistogram().Clone("new_sb")
hist_sb.Add(bkg, -1)
hist_sb.Draw("L same")

line = ro.TLine(105,0,160,0);
line.SetLineStyle(7); line.SetLineColor(1)
line.Draw("same")

c1.Update()
c1.Draw()
c1.Print("output/figures/bkg_subtracted.pdf]")
#c1.Close()




#name_list = [re.match("outfile.(.*?).root", file).group(1) for file in filenames]
#data = []
#mc = []
#for file in filenames:
#    a = re.match("outfile.(.*?).root", file).group(1)
#    if a.split("_")[0]=="data": data.append(file)
#    if a.split("_")[0]=="mc": mc.append(file)
