import ROOT as ro
import numpy as np
import sys, os
import re
from run_analysis import get_filenames, Quiet
from statistics import Poisson, CL, significance, pFromSig, sigFromP, test_sig
from ctypes import c_double
np.seterr(divide='ignore', invalid='ignore')
######################################################################
#   Path to your histograms if this is changed manually
#path = "/home/alida/Documents/uio/Master/FYS5555/project3/code/"
#d_path = path+"output/data/"
#m_path = path+"output/mc/"
#f_path = path+"output/figures/"

d_path = "output/data/"
m_path = "output/mc/"
f_path = "output/figures/"
#####################################################################
ro.gStyle.SetOptFit(1)
ro.gStyle.SetOptStat(0)
ro.gStyle.SetPadLeftMargin(0.13)
ro.gStyle.SetLegendBorderSize(1)
ro.gStyle.SetPalette(1)
ro.gStyle.SetGridStyle(2)
ro.gStyle.SetPadLeftMargin(0.13)
ro.TH1.AddDirectory(ro.kFALSE)
ro.gROOT.SetBatch(ro.kTRUE)
ro.gStyle.SetEndErrorSize(1.);
ro.gStyle.SetErrorX(ro.kFALSE)


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

# Print expected signal events from monte carlo
print("Expected signal events:\n")

error_tot = c_double()
total = dict_mc["combined"].IntegralAndError(0, 30, error_tot)
for key in dict_mc:
    er = c_double()
    #er = 1
    i = dict_mc[key].IntegralAndError(0, 30, er)
    if key == "combined": t = key
    else: t = key.split(".")[1].split("_")[0]
    print("{}: {:.2f}+-{:.2f} ({:.3f}%)".format(t,i, er.value, (i/total)*100))

hist_data = dict_data.get("combined")
hist_data.SetTitle("({}) ".format(cat)+"Invariant mass; m_{#gamma#gamma}; Events")
hist_mc = dict_mc.get("combined")
hist_mc.SetTitle("({}) ".format(cat)+"Invariant mass; m_{#gamma#gamma}; Events")
hist_stat = statistical_uncert(hist_mc)       # Get the statistical uncertainty

#######################################################################
#                        PLOTTING
#######################################################################

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

def conf(hist, xlow, xup):
    nbins = hist.GetNbinsX()
    #xlow = hist.GetXaxis().GetXmin()
    #xup = hist.GetXaxis().GetXmax()
    hint1 = ro.TH1D("hint", "Fitted gaussian with .95 conf.band", nbins, xlow, xup);
    hint2 = ro.TH1D("hint", "Fitted gaussian with .68 conf.band", nbins, xlow, xup);
    #Now the "hint" histogram has the fitted function values as the
    #bin contents and the confidence intervals as bin errors
    hint1.SetStats(ro.kFALSE)
    hint2.SetStats(ro.kFALSE)
    hint1.SetFillColor(ro.kYellow)
    hint2.SetFillColor(ro.kGreen)
    return hint1, hint2
#######################################################################
# Histogram stacks for mc and data
#######################################################################
#c0 = ro.TCanvas("stack", "stack", 800, 1200)
c0 = ro.TCanvas("stack", "stack", 800, 800)
c0.SetCanvasSize(800,800);
c0.Divide(1,2)

c0.cd(1)
mc_stack, mc_leg = stack_hist(dict_mc, "mc")
mc_stack.Draw("hist")
hist_stat.Draw("e2same")
mc_leg.AddEntry(hist_stat, "stat.unc.", "f")
mc_leg.Draw("")
c0.Update()
draw_atlas(0.6, 0.6, 0.044)

c0.cd(2)
data_stack, data_leg = stack_hist(dict_data, "data")
data_stack.Draw("hist")
data_leg.Draw()
draw_atlas(0.6,0.6,0.044)
c0.Update()
c0.Draw()
Quiet(c0.SaveAs)(f_path+cat+"_stacked_histograms.pdf]")
c0.Close()

#######################################################################
# Fitting signal, signal + background and drawing background model
#######################################################################
"""
c = ro.TCanvas("fitting", "fitting", 800, 800)
c.SetCanvasSize(800,800);
c.Divide(1,2)

c.cd(1) # signal fit
hmc = hist_mc.Clone("hmc")
hmc.Draw("E")
hmc.Fit("gaus", "q", "", 120, 130)    #Signal fit

draw_atlas(0.6,0.6,0.044)
hmc.SetTitle("({}) ".format(cat)+"Gaussian signal fit to MC")
func_s = hmc.GetFunction("gaus")
gaus_par = [func_s.GetParameter(i) for i in range(3)]

#Print fit statistics
print("\nGaussian fit to MC signal:")
print("--------------------------------------------------")
print ("Chi2/ndf:        ", "{:.4f}".format(func_s.GetChisquare()/func_s.GetNDF()))
print ("Prob:            ", "{:.4f}".format(func_s.GetProb()))

c.cd(2) # signal+background fit
sb = ro.TF1("s+b", "([0]+[1]*x+[2]*x^2+[3]*x^3)+[4]*exp(-0.5*((x-[5])/[6])^2)", 105, 160);
sb.SetTitle("Signal+Background fit"); #sb.SetLineColor(2); sb.SetLineStyle(1)
sb.FixParameter(4, gaus_par[0]);
sb.FixParameter(5,125.0);
sb.FixParameter(6, gaus_par[2]);

hd = hist_data.Clone("hd");
hd.SetTitle("({}) ".format(cat)+"Signal+background fit; m_{#gamma#gamma}; Events")

hd.Fit(sb, "qR")
hd.Draw("E")
draw_atlas(0.6,0.6,0.044)

func_sb = hd.GetFunction("s+b")
sb_par = [func_sb.GetParameter(i) for i in range(7)]

#Print fit statistics
print("\nSignal + background fit to data:")
print("--------------------------------------------------")
print ("Chi2/ndf:        ", "{:.4f}".format(func_sb.GetChisquare()/func_sb.GetNDF()))
print ("Prob:            ", "{:.4f}".format(func_sb.GetProb()))

c.Update();
Quiet(c.SaveAs)(f_path + cat +"_s_sb_fitting.pdf]")
c.Close()
"""
######################################################################
#   Signal fit
######################################################################
#Print fit statistics
print("\nPreforming Gaussian fit to Monte Carlo signal...")

hm = hist_mc.Clone("gaus fit")
hm.Fit("gaus", "q0", "", 120, 130)
func_s = hm.GetFunction("gaus")
h_sig = ro.TH1F("", "", 100, 120,130)
h_sig.Eval(func_s)

gaus_par = [func_s.GetParameter(i) for i in range(3)]
gaus_err = [func_s.GetParError(i) for i in range(3)]
c = ro.TCanvas("signal", "signal", 1000, 600)
c.SetCanvasSize(1000, 600)
ro.gStyle.SetOptFit(0)
hm.Draw("E")
func_s.Draw("L SAME")

chi2 = func_s.GetChisquare()
ndf = func_s.GetNDF()
sigma = gaus_par[-1]
mean = gaus_par[1]

fwhm = (2*np.sqrt(2*np.log(2)))*sigma
ymaximum = func_s.GetMaximum()
y2 = ymaximum/2
x1 = mean-(fwhm/2)
x2 = mean+(fwhm/2)
FWHM = ro.TLine(x1,y2,x2,y2)
FWHM.Draw()

xmin = mean-sigma
xmax = mean+sigma
low_x = ro.TLine(xmin, 0, xmin, 80)
low_x.SetLineStyle(7); low_x.SetLineColor(14)
high_x = ro.TLine(xmax, 0, xmax, 80)
high_x.SetLineStyle(7); high_x.SetLineColor(14)
low_x.Draw()
high_x.Draw()

eline = ro.TLine(0,0,0,0)
eline.SetLineStyle(0); eline.SetLineColor(0)

lsig = ro.TLegend(0.59,0.67,0.96,0.92)
lsig.SetTextSize(0.033)
lsig.AddEntry(hist_mc, "Monte Carlo Simulation")
lsig.AddEntry(func_s, "Signal fit (Gaussian)")
lsig.AddEntry(low_x, "#sigma = {:.2f} GeV".format(sigma), "l")
lsig.AddEntry(FWHM, "FWHM = {:.2f} GeV".format(fwhm), "l")

lsig.Draw()
draw_atlas(0.6,0.6,0.033)
c.Update()
c.Draw()
Quiet(c.SaveAs)(f_path+cat+"_signal_fit.pdf]")
c.Close()

print ("Chi2/ndf:        ", "{:.4f}".format(func_s.GetChisquare()/func_s.GetNDF()))
print ("Prob:            ", "{:.4f}".format(func_s.GetProb()))
#######################################################################
# Signal + bkg fit to data
#######################################################################

print("\nPreforming signal+background fit to data..")

c_sb = ro.TCanvas("sb","sb",1000,600)
c_sb.SetCanvasSize(1000,600)

sb = ro.TF1("s+b", "([0]+[1]*x+[2]*x^2+[3]*x^3)+[4]*exp(-0.5*((x-[5])/[6])^2)", 105, 160);
sb.SetTitle("Signal+Background fit"); #sb.SetLineColor(2); sb.SetLineStyle(1)
sb.FixParameter(4, gaus_par[0]);
sb.FixParameter(5,125.0);
sb.FixParameter(6, gaus_par[2]);

h_splusb = hist_data.Clone("splusb")
h_splusb.SetTitle("; m_{#gamma#gamma}; Events")
h_splusb.Sumw2();
h_splusb.Fit("s+b", "QR")

func_sb = h_splusb.GetFunction("s+b")
sb_par = [func_sb.GetParameter(i) for i in range(7)]

#Create Histogram of the model
h_sb = ro.TH1F("h_sb", "", 100, 105, 160)
h_sb.Eval(func_sb)

ro.gStyle.SetOptFit(0)
c_sb.Clear()

rp = ro.TRatioPlot(h_splusb, "diffsig")
rp.SetSeparationMargin(0.0);
rp.SetGraphDrawOpt("L");
rp.Draw()
rp.GetLowerRefYaxis().SetTitle("Residual");
rp.GetLowerRefYaxis().SetNdivisions(405)
rp.GetLowerRefGraph().SetMinimum(-3);
rp.GetLowerRefGraph().SetMaximum(3);
c_sb.Update()

hint1, hint2 = conf(h_splusb, 105,160)

ll = ro.TLegend(0.59,0.77,0.96,0.92)
ll.SetTextSize(0.033)
ll.AddEntry(hist_data, "Data")
ll.AddEntry(sb, "S+B fit (3rd order polynomial+gaussian)")
ll.AddEntry(hint1, "#pm 1#sigma")
ll.AddEntry(hint2, "#pm 2#sigma")

pad  = rp.GetUpperPad()
pad.cd()
draw_atlas(0.35,0.8,0.033)
ll.Draw()
pad.Modified()
pad.Update()
c_sb.Update()
Quiet(c_sb.SaveAs)(f_path+cat+"_sb_fit.pdf]")
c_sb.Close()

print ("Chi2/ndf:        ", "{:.1f}/{:.1f} = {:.4f}".format(func_sb.GetChisquare(),func_sb.GetNDF(),func_sb.GetChisquare()/func_sb.GetNDF()))
print ("Prob:            ", "{:.4f}".format(func_sb.GetProb()))
###############################################################################
# Background model from s+b
###############################################################################
bkg1 = ro.TF1("bkg1", "([0]+[1]*x+[2]*x^2+[3]*x^3)", 105, 160);
bkg1.SetTitle("({}) ".format(cat) + "Background model; m_{#gamma#gamma}; Events")
bkg1.SetParameter(0,sb_par[0])
bkg1.SetParameter(1,sb_par[1])
bkg1.SetParameter(2,sb_par[2])
bkg1.SetParameter(3,sb_par[3])
bkg1.SetLineStyle(7); bkg1.SetLineColor(4)

bkg = ro.TF1("bkg", "([0]+[1]*x+[2]*x^2+[3]*x^3)", 105, 160);
bkg.SetTitle("({}) ".format(cat) + "Background model; m_{#gamma#gamma}; Events")
bkg.FixParameter(0,sb_par[0])
bkg.FixParameter(1,sb_par[1])
bkg.FixParameter(2,sb_par[2])
bkg.FixParameter(3,sb_par[3])
bkg.SetLineStyle(7); bkg.SetLineColor(4)

#h_bkg = ro.TH1F("h_bkg", "h_bkg", 100, 105, 160)
#h_bkg.Eval(bkg)

#######################################################################
# Background only fit to data
#######################################################################
print("\nPreforming background only fit to data..")

c_bkgonly = ro.TCanvas("c_bkgonly", "c_bkgonly", 1000, 600)
c_bkgonly.SetCanvasSize(1000,600)

h_data_bkgfit = hist_data.Clone("h_data_bkgfit")
h_data_bkgfit.SetTitle("; m_{#gamma#gamma}; Events")
h_data_bkgfit.Sumw2();
h_data_bkgfit.Fit(bkg1, "RQ")
ro.gStyle.SetOptFit(0)
c_bkgonly.Clear()
func_bkg1 = h_data_bkgfit.GetFunction("bkg1")
#h_bkg1 = ro.TH1F("h_bkg", "h_bkg", 100, 105, 160)
#h_bkg1.Eval(func_bkg1)

rp1 = ro.TRatioPlot(h_data_bkgfit, "diff")
rp1.SetSeparationMargin(0.0);
rp1.SetGraphDrawOpt("L");
rp1.Draw()
rp1.GetLowerRefYaxis().SetTitle("Residual");
rp1.GetLowerRefYaxis().SetNdivisions(405)
rp1.GetLowerRefGraph().SetMinimum(-3);
rp1.GetLowerRefGraph().SetMaximum(3);
c_bkgonly.Update()

hint1, hint2 = conf(h_data_bkgfit, 105,160)

lll = ro.TLegend(0.59,0.77,0.96,0.92)
lll.SetTextSize(0.033)
lll.AddEntry(hist_data, "Data")
lll.AddEntry(bkg1, "Bkg-only fit (3rd order polynomial)")
lll.AddEntry(hint1, "#pm 1#sigma")
lll.AddEntry(hint2, "#pm 2#sigma")

pad  = rp1.GetUpperPad()
pad.cd()
draw_atlas(0.35,0.8,0.033)
lll.Draw()
pad.Modified()
pad.Update()
Quiet(c_bkgonly.SaveAs)(f_path+cat+"_bkg_only_fit.pdf]")
c_bkgonly.Close()

print ("Chi2/ndf:        ", "{:.1f}/{:.1f} = {:.4f}".format(func_bkg1.GetChisquare(),func_bkg1.GetNDF(),func_bkg1.GetChisquare()/func_bkg1.GetNDF()))
print ("Prob:            ", "{:.4f}".format(func_bkg1.GetProb()))

#######################################################################
# Plot both models with data, remove bkg
#######################################################################

c1 = ro.TCanvas("All", "All", 1000, 700);
c1.SetCanvasSize(1000,700);

pad0 = ro.TPad("pad0","pad0", 0,0.20,1,1,0,0,0);
pad0.SetFrameBorderMode(0)
pad1 = ro.TPad("pad1","pad1", 0,0,1,0.29,0,0,0);
pad1.SetTopMargin(0);
pad1.SetBottomMargin(0.3);
pad1.SetFrameBorderMode(0);
pad0.Draw()
pad1.Draw()

pad0.cd()
hist_data.Draw("E")
bkg.Draw("L same")
sb.Draw("L same")

l1 = ro.TLegend(0.59,0.77,0.96,0.92)
l1.SetTextSize(0.024)
l1.AddEntry(hist_data, "Data")
l1.AddEntry(bkg, "Bkg (3rd order polynomial)")
l1.AddEntry(sb, "Signal+background fit (m_{H} = 125 GeV)")
l1.Draw()
draw_atlas(0.35,0.8,0.033)

pad1.cd()
pad1.GetFrame().SetY1(2);

# Create line to illustrate the bkg
line_bkg = ro.TLine(105,0,160,0);
line_bkg.SetLineStyle(7); line_bkg.SetLineColor(4)

hist_sb_bkg_removed = h_sb.Clone("sb")
hist_sb_bkg_removed.SetLineColor(2)
hist_sb_bkg_removed.Sumw2()
hist_sb_bkg_removed.Add(bkg, -1)

hist_data_bkg_removed = hist_data.Clone("data-bkg")
hist_data_bkg_removed.SetTitle("; m_{#gamma#gamma}; Events - bkg ")
hist_data_bkg_removed.GetXaxis().SetTitleSize(0.1)
hist_data_bkg_removed.GetXaxis().SetLabelSize(0.1)
hist_data_bkg_removed.GetYaxis().SetTitleSize(0.1)
hist_data_bkg_removed.GetYaxis().SetTitleOffset(0.4)
hist_data_bkg_removed.GetYaxis().SetLabelSize(0.10)
hist_data_bkg_removed.Sumw2()
hist_data_bkg_removed.Add(bkg, -1)

hist_data_bkg_removed.Draw("E")
hist_data_bkg_removed.GetYaxis().SetNdivisions(405)
hist_sb_bkg_removed.Draw("L same")
line_bkg.Draw()

c1.Update();
c1.Draw()
Quiet(c1.SaveAs)(f_path+cat+"_bkg_subtracted.pdf]")
c1.Close()

#######################################################################
# Significance?
#######################################################################

h_bkg = ro.TH1F("hbkg", "; m_{#gamma#gamma}; Events", 30, 105, 160)
h_bkg.SetFillColor(41); h_bkg.SetLineStyle(1) ; h_bkg.SetLineColor(1); h_bkg.SetLineWidth(1)
h_bkg.Sumw2()
h_bkg.Eval(bkg)

h_bkg1 = ro.TH1F("hbkg1", "; m_{#gamma#gamma}; Events", 30, 105, 160)
h_bkg1.SetFillColor(41); h_bkg1.SetLineStyle(1) ; h_bkg1.SetLineColor(1); h_bkg1.SetLineWidth(1)
h_bkg1.Sumw2()
h_bkg1.Eval(bkg1)

h_bkg1 = ro.TH1F("hbkg", "; m_{#gamma#gamma}; Events", 30, 105, 160)
h_bkg1.SetFillColor(41); h_bkg1.SetLineStyle(1) ; h_bkg1.SetLineColor(1); h_bkg1.SetLineWidth(1)
h_bkg1.Sumw2()
h_bkg1.Eval(bkg1)

h_sig = ro.TH1F("hsig", "; m_{#gamma#gamma}; Events", 30, 105, 160)
h_sig.Sumw2()
h_sig.SetFillColor(46); h_sig.SetLineStyle(1); h_sig.SetLineColor(1); h_sig.SetLineWidth(1)
h_sig.Eval(func_sb)
h_sig.Add(h_bkg,-1)

h_dat = hist_data.Clone("h_dat")

def count_events(h1, h2, h3, low, high):
    x1 = h1.FindBin(low)
    x2 = h1.FindBin(high)
    n = h1.Integral(x1, x2)
    s = h2.Integral(x1, x2)
    b = h3.Integral(x1, x2)
    return n, s, b

print("\n---------------------------")
print("SINGAL+ BACKGROUND MODEL")
print("---------------------------")
n1, s1, b1 = count_events(h_dat, h_sig, h_bkg, 120, 130)
n2, s2, b2 = count_events(h_dat, h_sig, h_bkg, 110, 160)

exp_significance1, obs_significance1 = significance(s1, b1, n1)
exp_significance2, obs_significance2 = significance(s2, b2, n2)

p_exp1 = pFromSig(exp_significance1)
p_obs1 = pFromSig(obs_significance1)
p_exp2 = pFromSig(exp_significance2)
p_obs2 = pFromSig(obs_significance2)

print("In mass window +-5 GeV around 125 GeV:")
print("nobs = {:.1f}, s = {:.1f}, b = {:.1f}".format(n1, s1, b1))
print("expected: {:.2e} ({:.2f} sigma)".format(p_exp1, exp_significance1))
print("observed: {:.2e} ({:.2f} sigma)".format(p_obs1, obs_significance1))

print("\nIn the full mass range:")
print("nobs = {:.1f}, s = {:.1f}, b = {:.1f}".format(n2, s2, b2))
print("expected: {:.2e} ({:.2f} sigma)".format(p_exp2, exp_significance2))
print("observed: {:.2e} ({:.2f} sigma)".format(p_obs2, obs_significance2))

print("---------------------------")
print("BACKGROUND ONLY")
print("------------------------------")
n3, s3, b3 = count_events(h_dat, h_sig, h_bkg, 120, 130)
n4, s4, b4 = count_events(h_dat, h_sig, h_bkg, 110, 160)

exp_significance3, obs_significance3= significance(0, b3, n3)
exp_significance4, obs_significance4 = significance(0, b4, n4)

p_exp3 = pFromSig(exp_significance3)
p_obs3 = pFromSig(obs_significance3)
p_exp4 = pFromSig(exp_significance4)
p_obs4 = pFromSig(obs_significance4)

print("In mass window +-5 GeV around 125 GeV:")
print("nobs = {:.1f}, s = {:.1f}, b = {:.1f}".format(n3, s3, b3))
print("expected: {:.2e} ({:.2f} sigma)".format(p_exp3, exp_significance3))
print("observed: {:.2e} ({:.2f} sigma)".format(p_obs3, obs_significance3))

print("\nIn the full mass range:")
print("nobs = {:.1f}, s = {:.1f}, b = {:.1f}".format(n4, s4, b4))
print("expected: {:.2e} ({:.2f} sigma)".format(p_exp4, exp_significance4))
print("observed: {:.2e} ({:.2f} sigma)".format(p_obs4, obs_significance4))

"""
#mass_range = [120, 130]
liney = [3500, 800, 450, 300]
mass_low = ro.TLine(120,0,120,liney[category]);
mass_low.SetLineStyle(7); mass_low.SetLineColor(14)
mass_high = ro.TLine(130, 0, 130, liney[category]);
mass_high.SetLineStyle(7); mass_high.SetLineColor(14)

c2 =ro.TCanvas("d","d", 1000, 600)
c2.SetCanvasSize(1000,600);
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
l3.AddEntry(h_bkg, "Expected background")
l3.AddEntry(h_sig, "Expected signal(m_{H}=125 GeV)")
l3.AddEntry(h_dat,"Data", "p")
l3.AddEntry(mass_low, "Mass window", "l")
l3.Draw()

draw_atlas(0.4,0.86, 0.03)

t = ro.TLatex()
t.SetNDC(1)
t.SetTextAlign(13)
t.SetTextSize(0.030)
t.SetTextFont(42)
t.DrawLatex(0.64,0.70,"Events in mass window:")
t.DrawLatex(0.66,0.67,"b")      ; t.DrawLatex(0.7,0.67, "=  {:.2f}".format(b1))
t.DrawLatex(0.66,0.64,"s")      ; t.DrawLatex(0.7,0.64, "=  {:.2f}".format(s1))
t.DrawLatex(0.66,0.61,"n_{obs}"); t.DrawLatex(0.7,0.61, "=  {:.2f}".format(n1))
t.DrawLatex(0.64,0.58,"Expected significance:")
t.DrawLatex(0.66,0.55,"p = {:.4f} ({:.2f}#sigma)".format(p_exp, exp_significance))
t.DrawLatex(0.64,0.52,"Observed significance:")
t.DrawLatex(0.66,0.49,"p = {:.4f} ({:.2f}#sigma)".format(p_obs, obs_significance))
t.Draw()

c2.Update()
Quiet(c2.SaveAs)(f_path+cat+"_mass_window.pdf]")
#c2.Close()
"""
