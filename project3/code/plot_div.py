import ROOT as ro
import numpy as np
import sys, os
import re
from run_analysis import get_filenames, Quiet
import matplotlib.pyplot as plt

ro.gStyle.SetOptFit(1)
ro.gStyle.SetOptStat(0)
ro.gStyle.SetPadLeftMargin(0.13)
ro.gStyle.SetLegendBorderSize(1)
ro.gStyle.SetPalette(1)
ro.gStyle.SetGridStyle(2)
ro.gStyle.SetPadLeftMargin(0.13)
ro.TH1.AddDirectory(ro.kFALSE)
ro.gROOT.SetBatch(1)

def sort_files(filenames):
    name_list= [re.match("div.(.*?).root", file).group(1) for file in filenames]
    file_data = []
    file_mc = []
    for name, file in zip(name_list, filenames):
        if name.split("_")[0] == "data":
            file_data.append(file)
        else:
            file_mc.append(file)
    return file_data, file_mc

def get_hist(file, name):
    infile = ro.TFile(file)
    hist = ro.TH1F()
    hist = infile.Get(name).Clone("new_"+name)
    infile.Close()
    return hist

def make_dict(path, filenames, hist_names):
    name_list = [re.match("div.(.*?).root", file).group(1) for file in filenames]
    h1 = {}
    h2 = {}
    h3 = {}
    h4 = {}
    h5 = {}
    h6 = {}
    h7 = {}
    h8 = {}
    h9 = {}
    for name, file in zip(name_list, filenames):
        h1[name] = get_hist(path+file, hist_names[0])
        h2[name] = get_hist(path+file, hist_names[1])
        h3[name] = get_hist(path+file, hist_names[2])
        h4[name] = get_hist(path+file, hist_names[3])
        h5[name] = get_hist(path+file, hist_names[4])
        h6[name] = get_hist(path+file, hist_names[5])
        h7[name] = get_hist(path+file, hist_names[6])
        h8[name] = get_hist(path+file, hist_names[7])
        h9[name] = get_hist(path+file, hist_names[8])
    return h1, h2, h3, h4, h5 ,h6 ,h7, h8, h9

def stat_unc(hist):
    # Statistical uncertainty
    statistical_stack = hist.Clone("statistics")
    bins = statistical_stack.GetNbinsX()
    for i in range(bins):
        error = statistical_stack.GetBinError(i)
        statistical_stack.SetBinError(i, error)
    statistical_stack.SetFillStyle(3454);
    statistical_stack.SetFillColor(ro.kBlue+2);
    return statistical_stack

def stack_hist(dict, type, title):
    stack = ro.THStack("stack", title)
    combined_hist = combine(dict,type)
    unc = stat_unc(combined_hist)
    leg = ro.TLegend(0.66,0.70,0.96,0.92)
    leg.SetTextSize(0.025)
    if type == "mc":
        colours = [32,20,41,33,47]
    else:
        colours = [32,41,33,47]
    for key, i in zip(dict, colours):
        dict[key].SetFillColor(i)
        stack.Add(dict[key])
        leg.AddEntry(dict[key], "{}".format(key))
    return stack, leg, unc

def stack_hist2(dict, type, title):
    stack = ro.THStack("stack", title)
    leg = ro.TLegend(0.66,0.70,0.96,0.92)
    leg.SetTextSize(0.025)
    ours = [32,41,33,47]
    if type == "mc":
        colours = [221,213,205,209,128]
        #markers = [24,25,26,27,28]
        markers = [20,21,22,23,33]
    else:
        colours = [221,213,205,209]
        #markers = [24,25,26,27]
        markers = [20,21,22,23]
    for key, i,j in zip(dict, colours, markers):
        dict[key].SetFillColor(i)
        #dict[key].SetFillStyle(3454)
        dict[key].SetMarkerStyle(j)
        dict[key].SetMarkerColor(i)
        dict[key].SetLineColor(ro.kBlack)
        stack.Add(dict[key])
        leg.AddEntry(dict[key], "{}".format(key))
    return stack, leg

def combine(dict, option):
    keys = [key for key in dict]
    hist = dict[keys[0]].Clone("clone")
    hist.Add(dict[keys[1]])
    hist.Add(dict[keys[2]])
    hist.Add(dict[keys[3]])
    if option =="mc":
        hist.Add(dict[keys[4]])
    return hist

##########################################################################
hist_names = ["hist_pt1", "hist_pt2", "hist_eta1", "hist_eta2", "hist_energy1",
                "hist_energy2", "hist_dPhi", "hist_kincut0", "hist_kincut1"]

path = "/home/alida/Documents/uio/Master/FYS5555/project3/code/output/"
f_path = path+"figures/"
filenames = get_filenames(path)

file_data, file_mc = sort_files(filenames)
###########################################################################

def plot_lorentz(path, file, hist_names, option):
    pt1, pt2, eta1, eta2, energy1, energy2, dPhi, kincut0, kincut1= make_dict(path, file, hist_names)

    lead_pt, leg1, unc1 = stack_hist(pt1, option, " ;p_{T}^{leading}; Events")
    lead_eta, leg2, unc1 = stack_hist(eta1, option, " ;#eta^{leading}; Events")
    lead_energy, leg3, unc1= stack_hist(energy1, option, " ;E^{leading}; Events")

    sub_pt, leg4, unc1= stack_hist(pt2, option, " ;p_{T}^{sub}; Events")
    sub_eta, leg5, unc1= stack_hist(eta2, option, " ;#eta^{sub}; Events")
    sub_energy, leg6, unc1= stack_hist(energy2, option, " ;E^{sub}; Events")

    c = ro.TCanvas("c"+option,"c"+option, 600, 1200)
    c.Divide(2,3)
    c.cd(1)
    lead_pt.Draw("hist")
    leg1.Draw()
    c.cd(3)
    lead_eta.Draw("hist")
    leg2.Draw()
    c.cd(5)
    lead_energy.Draw("hist")
    leg3.Draw()
    c.cd(2)
    sub_pt.Draw("hist")
    leg4.Draw()
    c.cd(4)
    sub_eta.Draw("hist")
    leg5.Draw()
    c.cd(6)
    sub_energy.Draw("hist")
    leg6.Draw()
    c.Update()
    #c.Draw()
    Quiet(c.Print)(f_path+"CP1_"+option+"_PtEtaE.pdf]")
    return c

#pt1, pt2, eta1, eta2, energy1, energy2, dPhi, kincut0, kincut1 = make_dict(path, file_data, hist_names)
#c_ptetaE_data = plot_lorentz(path, file_data, hist_names, "data")
#c_ptetaE_mc = plot_lorentz(path, file_mc, hist_names, "mc")
###########################################################################

def plot_kincut(data, mc):
    kin_cut0 = combine(data[7], "data")
    kin_cut1 = combine(data[8], "data")
    kin_cut00 = combine(mc[7], "mc")
    kin_cut11 = combine(mc[8], "mc")

    kin_cut0.SetTitle("data;E_{T}/m_{#gamma#gamma}; Events")
    kin_cut0.SetMarkerStyle(22)
    kin_cut0.SetMarkerColor(221)
    kin_cut0.SetFillStyle(0)
    kin_cut1.SetTitle(";E_{T}/m_{#gamma#gamma}; Events")
    kin_cut1.SetMarkerStyle(23)
    kin_cut1.SetMarkerColor(213)
    kin_cut1.SetFillStyle(0)

    kin_cut00.SetTitle("MC;E_{T}/m_{#gamma#gamma}; Events")
    kin_cut00.SetMarkerStyle(22)
    kin_cut00.SetMarkerColor(221)
    kin_cut00.SetFillStyle(0)
    kin_cut11.SetTitle(";E_{T}/m_{#gamma#gamma}; Events")
    kin_cut11.SetMarkerStyle(23)
    kin_cut11.SetMarkerColor(213)
    kin_cut11.SetFillStyle(0)

    c = ro.TCanvas("c2", "c2", 600, 1200)
    c.Divide(1,2)
    c.cd(1)
    kin_cut0.Draw("E hist")
    kin_cut1.Draw("E hist same")
    leg = ro.TLegend(0.66,0.70,0.96,0.92)
    leg.SetTextSize(0.025)
    leg.AddEntry(kin_cut0, "Before cut on E_{T}/m_{#gamma#gamma}", "p")
    leg.AddEntry(kin_cut1, "After cut E_{T}/m_{#gamma#gamma}", "p")
    leg.Draw()
    c.cd(2)
    kin_cut00.Draw("E hist")
    kin_cut11.Draw("E hist same")
    leg1 = ro.TLegend(0.66,0.70,0.96,0.92)
    leg1.SetTextSize(0.025)
    leg1.AddEntry(kin_cut0, "Before cut on E_{T}/m_{#gamma#gamma}", "p")
    leg1.AddEntry(kin_cut1, "After cut E_{T}/m_{#gamma#gamma}", "p")
    leg1.Draw()
    c.Update()
    c.Draw()
    Quiet(c.Print)(f_path + "CP1_kin_cut.pdf]")
    #c.Close()
    return c

data = make_dict(path, file_data, hist_names)
mc = make_dict(path, file_mc, hist_names)

#c_kin = plot_kincut(data, mc)

#############################################################################

def plot_dphi(data, mc):
    hist_dPhi1 = combine(data[6], "data")
    hist_dPhi1.SetMarkerStyle(20)
    hist_dPhi1.SetMarkerColor(221)

    hist_dPhi2 = combine(mc[6], "mc")
    hist_dPhi2.SetMarkerStyle(20)
    hist_dPhi2.SetMarkerColor(213)

    l1 = ro.TLegend(0.66,0.80,0.96,0.92)
    l1.SetTextSize(0.025)
    l2 = ro.TLegend(0.66,0.80,0.96,0.92)
    l2.SetTextSize(0.025)

    c = ro.TCanvas("dphi", "dphi", 600, 1200)
    c.Divide(1,2)
    c.cd(1)
    hist_dPhi1.Draw("EL")
    l1.AddEntry(hist_dPhi1, "Data", "p")
    l1.Draw()
    c.cd(2)
    hist_dPhi2.Draw("EL")
    l2.AddEntry(hist_dPhi2, "Monte Carlo", "p")
    l2.Draw()

    c.Update()
    c.Draw()
    Quiet(c.Print)(f_path+"CP1_dPhi.pdf]")
    return c

c_dphi = plot_dphi(data, mc)

"""
pt1
pt2
eta1
eta2
energy1
energy2
dPhi
kincut0
kincut1
"""
