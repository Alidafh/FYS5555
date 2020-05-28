import ROOT as ro
import numpy as np
import sys, os
import re
from run_analysis import get_filenames, Quiet

######################################################################
#   Path to your data
path = "/home/alida/Documents/uio/Master/FYS5555/project3/code/"
d_path = path+"output/data/"
m_path = path+"output/mc/"
f_path = path+"output/figures/"
#####################################################################
ro.gStyle.SetOptFit(1)
ro.gStyle.SetOptStat(0)
ro.gStyle.SetPadLeftMargin(0.13)
ro.gStyle.SetLegendBorderSize(1)
ro.gStyle.SetPalette(1)
ro.gStyle.SetGridStyle(2)
ro.gStyle.SetPadLeftMargin(0.13)
ro.TH1.AddDirectory(ro.kFALSE)
ro.gROOT.SetBatch(1)
ro.gStyle.SetEndErrorSize(1.);


def get_hist(file, name):
    infile = ro.TFile(file)
    hist = ro.TH1F()
    hist = infile.Get(name).Clone("new_"+name)
    infile.Close()
    return hist

def make_dict(path, filenames, title):
    name_list = [re.match("outfile.(.*?).root", file).group(1) for file in filenames]
    hist_CP1_tmp = {}
    hist_CP2_tmp = {}
    hist_CP3_tmp = {}
    hist_CP4_tmp = {}
    for name, file in zip(name_list,filenames):
        hist_CP1_tmp[name] = get_hist(path+file, "hist_mass_CP1")
        hist_CP1_tmp[name].SetTitle(title)
        hist_CP2_tmp[name] = get_hist(path+file, "hist_mass_CP2")
        hist_CP2_tmp[name].SetTitle(title)
        hist_CP3_tmp[name] = get_hist(path+file, "hist_mass_CP3")
        hist_CP3_tmp[name].SetTitle(title)
        hist_CP4_tmp[name] = get_hist(path+file, "hist_mass_CP4")
        hist_CP4_tmp[name].SetTitle(title)
    h1 = ro.TH1F("a1", "a1", 30, 105, 160)
    h2 = ro.TH1F("a2", "a2", 30, 105, 160)
    h3 = ro.TH1F("a3", "a3", 30, 105, 160)
    h4 = ro.TH1F("a4", "a4", 30, 105, 160)
    for k1, k2,k3, k4 in zip(hist_CP1_tmp, hist_CP2_tmp, hist_CP3_tmp, hist_CP4_tmp):
        h1.Add(hist_CP1_tmp[k1])
        h2.Add(hist_CP2_tmp[k2])
        h3.Add(hist_CP3_tmp[k3])
        h4.Add(hist_CP4_tmp[k4])
    hist_CP1_tmp["combined"] = h1.Clone("hist_CP1")
    hist_CP1_tmp["combined"].SetMarkerStyle(20)
    hist_CP1_tmp["combined"].SetTitle(title)
    hist_CP2_tmp["combined"] = h2.Clone("hist_CP2")
    hist_CP2_tmp["combined"].SetMarkerStyle(20)
    hist_CP2_tmp["combined"].SetTitle(title)
    hist_CP3_tmp["combined"] = h3.Clone("hist_CP3")
    hist_CP3_tmp["combined"].SetMarkerStyle(20)
    hist_CP3_tmp["combined"].SetTitle(title)
    hist_CP4_tmp["combined"] = h4.Clone("hist_CP4")
    hist_CP4_tmp["combined"].SetMarkerStyle(20)
    hist_CP4_tmp["combined"].SetTitle(title)
    return hist_CP1_tmp, hist_CP2_tmp, hist_CP3_tmp, hist_CP4_tmp

def stack_hist(dict, type):
    stack = ro.THStack("stack", "({})".format(cat)+"Stacked histograms from "+"{}".format(type)+"; m_{#gamma#gamma}; Events")
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
    return stack, leg

def statistical_uncert(hist):
    """Get the statistical uncertainty """
    hist_stat = hist.Clone("statistics")
    bins = hist_stat.GetNbinsX()
    for i in range(bins):
        error = hist_stat.GetBinError(i)
        hist_stat.SetBinError(i, error)
    hist_stat.SetFillStyle(3454);
    hist_stat.SetFillColor(ro.kBlue+2);
    hist_stat.SetMarkerStyle(0)
    return hist_stat

######################################################################
data_filenames = get_filenames(d_path)
mc_filenames = get_filenames(m_path)

data_categories = make_dict(d_path, data_filenames, "Invariant mass; m_{#gamma#gamma};Events")
mc_categories = make_dict(m_path, mc_filenames, "Invariant mass; m_{#gamma#gamma};Events")

#######################################################################
# What mode the program is run for: 0 - CP1, 1 - CP2, 2 - CP3 3 - CP4

category = int(sys.argv[1])

catNames = ["Inclusive", "Central inclusive", "Central unconverted", "Central converted"]
catTypes = ["CP1", "CP2", "CP3", "CP4"]

print("\n--------------------------------------------------")
print("Plotting for {}: {}".format(catTypes[category], catNames[category]))
print("--------------------------------------------------")

dict_mc = mc_categories[category]
dict_data = data_categories[category]
cat = catTypes[category]

#Print expected signal events from monte carlo
print("Expected signal events:\n")
for key in dict_mc:
    i = dict_mc[key].Integral()
    if key == "combined": t = key
    else: t = key.split(".")[1].split("_")[0]
    print("{}:     {}".format(t,i))

#######################################################################
#                        PLOTTING
#######################################################################

hist_data = dict_data.get("combined").Clone("fit data")
hist_data.SetTitle("({}) ".format(cat)+"Invariant mass; m_{#gamma#gamma}; Events")
hist_mc = dict_mc.get("combined").Clone("fit mc")
hist_data.SetTitle("({}) ".format(cat)+"Invariant mass; m_{#gamma#gamma}; Events")
hist_stat = statistical_uncert(hist_mc)       # Get the statistical uncertainty

def draw_atlas(x, y, text):
    """ Function to draw atlas open data label on the plots"""
    atlas = ro.TLatex()
    atlas.SetNDC(1);
    atlas.SetTextAlign(13);
    atlas.SetTextSize(text);
    atlas.SetTextFont(42);
    #atlas.DrawLatex(x,y,"#font[72]{ATLAS} Open Data, H #rightarrow #gamma#gamma");
    atlas.DrawLatex(x,y,"ATLAS Open Data, H #rightarrow #gamma#gamma");
    atlas.DrawLatex(x,y-0.06,"#sqrt{s} = 13 TeV, #int L dt = 10 fb^{-1}");
    atlas.Draw()

#######################################################################
# Histogram stacks for mc and data
#######################################################################
c0 = ro.TCanvas("stack", "stack", 800, 1200)
c0.Divide(1,2)

c0.cd(1)
mc_stack, mc_leg = stack_hist(dict_mc, "mc")
mc_stack.Draw("hist")
hist_stat.Draw("e2same")
mc_leg.AddEntry(hist_stat, "stat.unc.", "f")
mc_leg.Draw("")
c0.Update()
ro.gPad.SetLogy(1)
draw_atlas(0.6, 0.6, 0.044)

c0.cd(2)
data_stack, data_leg = stack_hist(dict_data, "data")
data_stack.Draw("hist")
data_leg.Draw()
draw_atlas(0.6,0.6,0.044)
c0.Update()
#c0.Draw()
Quiet(c0.Print)(f_path+cat+"_stacked_histograms.pdf]")
#c0.Print(f_path+cat+"_stacked_histograms.pdf]")
#c0.Close()

#######################################################################
# Fitting signal, signal + background and drawing background model
#######################################################################
c = ro.TCanvas("fitting", "fitting", 533, 1200)
c.Divide(1,3)

c.cd(1) # signal fit
hmc = hist_mc.Clone("hmc")
hmc.Draw("E same")
#hmc.SetAxisRange(0, 100, "Y")
hmc.Fit("gaus", "qWL", "", 121, 129)    #Signal fit
draw_atlas(0.6,0.6,0.044)
hmc.SetTitle("({}) ".format(cat)+"Gaussian signal fit to MC")
gaus_par = [hmc.GetFunction("gaus").GetParameter(i) for i in range(3)]

c.cd(2) # signal+background fit
sb = ro.TF1("s+b", "([0]+[1]*x+[2]*x^2+[3]*x^3)+[4]*exp(-0.5*((x-[5])/[6])^2)", 105, 160);
sb.SetTitle("Signal+Background fit"); sb.SetLineColor(2); sb.SetLineStyle(1)
sb.FixParameter(4, gaus_par[0]);
sb.FixParameter(5,125.0);
sb.FixParameter(6, gaus_par[2]);
hd = hist_data.Clone("hd");
hd.SetTitle("({}) ".format(cat)+"Signal+background fit (m_{H} = 125 GeV); m_{#gamma#gamma}; Events")

hd.Draw("E")
hd.Fit(sb, "qRL")
draw_atlas(0.6,0.6,0.044)
#draw_atlas(0.4,0.8,0.044)
func_sb = hd.GetFunction("s+b")
sb_par = [func_sb.GetParameter(i) for i in range(7)]

hist_sb = ro.TH1F("sb", "({}) ".format(cat)+"Signal+Background model;m_{#gamma#gamma}; Events", 30, 105, 160) # Create a histogram of the model
hist_sb.Eval(func_sb)
hist_sb.SetLineWidth(2);
hist_sb.SetLineColor(ro.kRed)

c.cd(3) # Background model
bkg = ro.TF1("bkg", "([0]+[1]*x+[2]*x^2+[3]*x^3)", 105, 160);
bkg.SetTitle("({}) ".format(cat) + "Background model; m_{#gamma#gamma}; Events")
bkg.SetParameter(0,sb_par[0])
bkg.SetParameter(1,sb_par[1])
bkg.SetParameter(2,sb_par[2])
bkg.SetParameter(3,sb_par[3])

hist_bkg = ro.TH1F("hbkg", "({}) ".format(cat)+"Background model; m_{#gamma#gamma}; Events", 30, 105, 160)
hist_bkg.Eval(bkg)
hist_bkg.SetLineStyle(7); hist_bkg.SetLineColor(4)

hd1 = hist_data.Clone("hd1")
bkg.Draw("L")
hd1.Draw("E same")
draw_atlas(0.6,0.6,0.044)
l0 = ro.TLegend(0.63,0.77,0.96,0.92)
l0.SetTextSize(0.04)
l0.AddEntry(hd1, "Data", "P")
l0.AddEntry(bkg, "Background model (3rd polynomial)")
l0.Draw()
c.Update();
#c.Draw();
Quiet(c.Print)(f_path + cat +"_s_sb_fitting.pdf]")
#c.Print(f_path + cat +"_s_sb_fitting.pdf]")
#c.Close()

#######################################################################
# Plot all models with data, remove bkg
#######################################################################

c1 = ro.TCanvas("All", "All", 800, 1200);
c1.Divide(1,2)

c1.cd(1)
hist_data.Draw("E")
hist_bkg.Draw("L same")
hist_sb.Draw("L same")

l1 = ro.TLegend(0.66,0.77,0.96,0.92)
l1.SetTextSize(0.033)
l1.AddEntry(hist_data, "Data")
l1.AddEntry(hist_bkg, "Bkg (3rd order polynomial)")
l1.AddEntry(hist_sb, "Signal+background (m_{H} = 125 GeV)")
l1.Draw()
draw_atlas(0.4,0.8,0.044)

c1.cd(2)
c1.GetFrame().SetY1(2);
line = ro.TLine(105,0,160,0); line.SetLineStyle(7); line.SetLineColor(4)

hist_sbNoB = hist_sb.Clone("sb-bkg")
hist_sbNoB.SetTitle("s+b model - background; m_{#gamma#gamma}; Events - bkg ")
hist_sbNoB.Add(hist_bkg, -1)

hist_signal = hist_data.Clone("data-bkg")
hist_signal.SetTitle("({}) ".format(cat)+"Expected background removed; m_{#gamma#gamma}; Events - bkg ")
hist_signal.Add(hist_bkg, -1)

hist_signal.Draw("E")
hist_sbNoB.Draw("L same")
line.Draw("L same")

draw_atlas(0.7,0.85,0.037)

c1.Update();
#c1.Draw()
Quiet(c1.Print)(f_path+cat+"_bkg_subtracted.pdf]")
#c1.Close()

#######################################################################
# Significance:
#######################################################################

np.seterr(divide='ignore', invalid='ignore')

def significance(s, b, n):
    Z_exp = np.nan_to_num(np.sqrt(2*(s+b)*np.log(1+(s/b)) - 2*s))
    Z_obs = np.nan_to_num(np.sqrt(2*n*np.log(n/b) - 2*(n-b)))
    return Z_exp, Z_obs

h_sig = hist_sbNoB.Clone("signal"); h_sig.SetTitle("Expected signal (m_{H} = 125 GeV) ")
h_sig.SetFillColor(46); h_sig.SetLineStyle(1); h_sig.SetLineColor(1); h_sig.SetLineWidth(1)
h_bkg = hist_bkg.Clone("background"); h_bkg.SetTitle("Expected background")
h_bkg.SetFillColor(41); h_bkg.SetLineStyle(1) ; h_bkg.SetLineColor(1); h_bkg.SetLineWidth(1)
h_dat = hist_data.Clone("data"); h_dat.SetTitle("Observed data")

mass_range= [121,129]
mass_window = [h_dat.FindBin(mass_range[0]), h_dat.FindBin(mass_range[-1])]

s = 0; b = 0; nobs = 0;
for i in range(mass_window[0], mass_window[-1]+1):
    s += h_sig.GetBinContent(i)
    b += h_bkg.GetBinContent(i)
    nobs += h_dat.GetBinContent(i)

exp_significance, obs_significance = significance(s,b,nobs)

mass_low = ro.TLine(mass_range[0],0,mass_range[0],800);
mass_low.SetLineStyle(7); mass_low.SetLineColor(14)
mass_high = ro.TLine(mass_range[-1], 0, mass_range[-1], 800);
mass_high.SetLineStyle(7); mass_high.SetLineColor(14)

c2 =ro.TCanvas("d","d", 1000, 900)
c2.cd()

stack3 = ro.THStack("s3", "({}) ".format(cat)+"Invariant mass distribution; m_{#gamma#gamma} [GeV]; Events")
stack3.Add(h_bkg)
stack3.Add(h_sig)
stack3.Draw("hist")
h_dat.Draw("E same")
mass_low.Draw("same")
mass_high.Draw("same")

l3 = ro.TLegend(0.66,0.77,0.96,0.92)
l3.SetTextSize(0.024)
l3.AddEntry(h_bkg)
l3.AddEntry(h_sig)
l3.AddEntry(h_dat,"", "p")
l3.AddEntry(mass_low, "Mass window", "l")
l3.Draw()

draw_atlas(0.4,0.86, 0.022)

t = ro.TLatex()
t.SetNDC(1)
t.SetTextAlign(13)
t.SetTextSize(0.022)
t.SetTextFont(42)
t.DrawLatex(0.64,0.66,"Events in mass window:")
t.DrawLatex(0.66,0.63,"b")      ; t.DrawLatex(0.7,0.63, "=  {:.2f}".format(b))
t.DrawLatex(0.66,0.60,"s")      ; t.DrawLatex(0.7,0.60, "=  {:.2f}".format(s))
t.DrawLatex(0.66,0.57,"n_{obs}"); t.DrawLatex(0.7,0.57, "=  {:.2f}".format(b))
t.DrawLatex(0.64,0.54,"Expected significance: {:.2f}".format(exp_significance)+"#sigma")
t.DrawLatex(0.64,0.50,"Observed significance: {:.2f}".format(obs_significance)+"#sigma")
t.Draw()
#c2.Draw()
Quiet(c2.Print)(f_path+cat+"_mass_window.pdf]")
#c2.Close()
