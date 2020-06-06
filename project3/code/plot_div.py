import ROOT as ro
import numpy as np
import sys, os
import re
from run_analysis import get_filenames, Quiet
import matplotlib.pyplot as plt

ro.gStyle.SetOptFit(1)
ro.gStyle.SetOptStat(0)
ro.gStyle.SetPadLeftMargin(0.13)
#ro.gStyle.SetPadBottomMargin(0.1)
#ro.gStyle.SetFrameBorderMode(0);
ro.gStyle.SetLegendBorderSize(1)
ro.gStyle.SetPalette(1)
ro.gStyle.SetGridStyle(2)
ro.TH1.AddDirectory(ro.kFALSE)
ro.gStyle.SetErrorX(ro.kFALSE)
ro.gROOT.SetBatch(ro.kTRUE)

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
                "hist_energy2", "hist_dPhi", "hist_phi1", "hist_phi2"]

path = "output/"
f_path = path+"figures/"
filenames = get_filenames(path)

file_data, file_mc = sort_files(filenames)
###########################################################################
###########################################################################
data = make_dict(path, file_data, hist_names)
mc = make_dict(path, file_mc, hist_names)

def norm(hist, option, fix):
    norm = 1
    scale = norm/(hist.Integral())
    hist.Scale(scale)
    hist.GetYaxis().SetTitle("Events, normalised")
    if option == "data":
        hist.SetMarkerStyle(24)
        hist.SetMarkerColor(1)
    else:
        hist.SetMarkerStyle(23)
        hist.SetMarkerColor(221)
    #if fix == 0:
        #hist.GetYaxis().SetLabelSize(0.05)
        #hist.GetYaxis().SetTitleSize(0.07)
        #hist.GetYaxis().SetTitleOffset(1)
        #hist.GetXaxis().SetLabelSize(0.05)
        #hist.GetXaxis().SetLabelOffset(0.03)
        #hist.GetXaxis().SetTitleSize(0.07)
        #hist.GetXaxis().SetTitleOffset(1.4)
    return hist

def plot_lorentz(data, mc):
    data_p1 = norm(combine(data[0], "data"), "data", 0)
    data_p2  = norm(combine(data[1], "data"), "data",0)
    data_eta1 = norm(combine(data[2], "data"), "data",0)
    data_eta2 = norm(combine(data[3], "data"), "data",0)
    data_E1 = norm(combine(data[4], "data"), "data",0)
    data_E2 = norm(combine(data[5], "data"), "data",0)
    data_phi1 = norm(combine(data[7], "data"), "data",0)
    data_phi2 = norm(combine(data[8], "data"), "data",0)

    mc_p1 = norm(combine(mc[0], "mc"), "mc",0)
    mc_p2  = norm(combine(mc[1], "mc"), "mc",0)
    mc_eta1 = norm(combine(mc[2], "mc"), "mc",0)
    mc_eta2 = norm(combine(mc[3], "mc"), "mc",0)
    mc_E1 = norm(combine(mc[4], "mc"), "mc",0)
    mc_E2 = norm(combine(mc[5], "mc"), "mc",0)
    mc_phi1 = norm(combine(mc[7], "mc"), "mc",0)
    mc_phi2 = norm(combine(mc[8], "mc"), "mc",0)

    ro.gStyle.SetPadTopMargin(0)
    ro.gStyle.SetPadBottomMargin(0.3)

    l1 = ro.TLegend(0.80,0.70,0.96,0.84)
    l1.SetTextSize(0.042)
    l1.AddEntry(data_p1, "Data", "p")
    l1.AddEntry(mc_p1, "MC", "p")

    j = ro.TCanvas("j", "j", 900, 1200)
    j.SetCanvasSize(900,1200);
    j.Divide(2, 4, 0.01, 0.01)

    j.cd(1)
    data_p1.Draw("E")
    mc_p1.Draw("E same")
    l1.Draw()
    j.cd(2)
    data_p2.Draw("E")
    mc_p2.Draw("E same")
    l1.Draw()
    j.cd(3)
    data_eta1.Draw("E")
    mc_eta1.Draw("E same")
    l1.Draw()
    j.cd(4)
    data_eta2.Draw("E")
    mc_eta2.Draw("E same")
    l1.Draw()
    j.cd(5)
    data_E1.Draw("E")
    mc_E1.Draw("E same")
    l1.Draw()
    j.cd(6)
    data_E2.Draw("E")
    mc_E2.Draw("E same")
    l1.Draw()
    j.cd(7)
    data_phi1.Draw("E")
    mc_phi1.Draw("E same")
    l1.Draw()
    j.cd(8)
    data_phi2.Draw("E")
    mc_phi2.Draw("E same")
    l1.Draw()
    j.Update()
    Quiet(j.SaveAs)(f_path+"CP1_PtEtaE.pdf]")
    return j

c_lor = plot_lorentz(data, mc)
#############################################################################

def plot_dphi(data, mc):
    hist_dPhi1 = norm(combine(data[6], "data"), "data",1)

    hist_dPhi2 = norm(combine(mc[6], "mc"), "mc",1)

    l1 = ro.TLegend(0.80,0.80,0.96,0.92)
    l1.SetTextSize(0.025)
    l1.AddEntry(hist_dPhi1, "Data", "p")
    l1.AddEntry(hist_dPhi2, "MC(m_{H} = 125 GeV)", "p")
    c = ro.TCanvas("dphi", "dphi", 800, 500)
    c.SetCanvasSize(800,500);
    c.SetTopMargin(0.1)
    c.SetBottomMargin(0.1)
    hist_dPhi1.Draw("E1")
    hist_dPhi2.Draw("E1 same")
    l1.Draw()
    c.Update()
    c.Draw()
    Quiet(c.SaveAs)(f_path+"CP1_dPhi.pdf]")
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
