import ROOT as ro
import sys, os
import re
from run_analysis import get_filenames

def get_hist(file, name):
    infile = ro.TFile(file)
    hist = ro.TH1F()
    hist = infile.Get(name).Clone("new_"+name)
    hist.SetDirectory(0)
    infile.Close()
    return hist

def add(hist):
    hist_tmp = ro.TH1F("all", "all", 30,105,160)
    for key in hist:
        hist_tmp.Add(hist[key])
    return hist_tmp

def make_dict(path,filenames):
    name_list = [re.match("outfile.(.*?).root", file).group(1) for file in filenames]
    hist_all_tmp = {}
    hist_unc_tmp = {}
    for name, file in zip(name_list,filenames):
        #print(name, file)
        hist_all_tmp[name] = get_hist(path+file, "hist_mass_all")
        hist_unc_tmp[name] = get_hist(path+file, "hist_mass_unconv")
    return hist_all_tmp, hist_unc_tmp

hist_names = ["hist_mass_all", "hist_mass_unconv"]
path = "/home/alida/Documents/uio/Master/FYS5555/project3/code/output/"
d_path = path+"data/"
m_path = path+"mc/"

data_filenames = get_filenames(d_path)
mc_filenames = get_filenames(m_path)

dict_hist_data, dict_hist_unc_data = make_dict(d_path, data_filenames)
dict_hist_mc, dict_hist_unc_mc = make_dict(m_path, mc_filenames)

#hist_all_data = add(dict_hist_data)
hist_all_mc = add(dict_hist_mc)
#hist_unc_data = add(dict_hist_unc_data)
#hist_unc_mc = add(dict_hist_unc_mc)
c1 = ro.TCanvas("c1", "c1", 1000, 600)
c1.cd()
hist_all_mc.Draw("*H")
hist_all_mc.Fit("gaus","L")
c1.Update()
c1.Draw()


"""
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
