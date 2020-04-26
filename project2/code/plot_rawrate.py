import ROOT
from array import array
import sys
from os import listdir
from os.path import isfile, join
from datetime import datetime
import math
import numpy as np
ROOT.TH1.SetDefaultSumw2()

start_time = ROOT.TTimeStamp(2018,7,21,0,0,0)
stop_time  = ROOT.TTimeStamp(2018,9,5,0,0,0)
# The time offset used in the POLA data is 1st of January 2007
t = ROOT.TTimeStamp(2007,1,1,0,0,0)
da = ROOT.TDatime(2007,1,1,0,0,0)
ROOT.gStyle.SetTimeOffset(da.Convert());

def readfile(filename):
    data = np.loadtxt("{}".format(filename))
    x = data[:,0]
    y = data[:,1]
    x_rawrate = array('d')
    y_rawrate = array('d')
    for i in range(len(x)):
        x_rawrate.append(x[i])
        y_rawrate.append(y[i])
    return x_rawrate, y_rawrate

x1_rawrate, y1_rawrate = readfile("rawrate_01.txt")
x2_rawrate, y2_rawrate = readfile("rawrate_02.txt")
x3_rawrate, y3_rawrate = readfile("rawrate_03.txt")

C = ROOT.TCanvas("c", "c", 1200, 600)
C.SetGrid()
mg = ROOT.TMultiGraph("mg","mg")

g_RawRate1 = ROOT.TGraph(len(x1_rawrate), x1_rawrate, y1_rawrate)
g_RawRate1.SetMarkerStyle(20)
g_RawRate1.SetMarkerColor(1)
g_RawRate1.SetTitle("POLA-01")

g_RawRate2 = ROOT.TGraph(len(x2_rawrate), x2_rawrate, y2_rawrate)
g_RawRate2.SetMarkerStyle(20)
g_RawRate2.SetMarkerColor(2)
g_RawRate2.SetTitle("POLA-02")

g_RawRate3 = ROOT.TGraph(len(x3_rawrate), x3_rawrate, y3_rawrate)
g_RawRate3.SetMarkerStyle(20)
g_RawRate3.SetMarkerColor(4)
g_RawRate3.SetTitle("POLA-03")

mg.Add(g_RawRate1)
mg.Add(g_RawRate2)
mg.Add(g_RawRate3)
mg.Draw("AP")
mg.SetTitle("Raw Rate over time")
mg.GetXaxis().SetTimeDisplay(1)
mg.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
mg.GetXaxis().SetLabelOffset(0.03)
mg.GetYaxis().SetTitle("Raw Rate")
mg.GetYaxis().SetLabelOffset(0.01)
mg.GetYaxis().SetTitleOffset(1.1);
legend = C.BuildLegend(0.73,0.3,0.9,0.4)
legend.SetFillStyle(0)
legend.SetBorderSize(0)
C.Update()
C.Print("../figures/RawRate_time_all.pdf]")
C.Draw()
