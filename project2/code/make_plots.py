import ROOT
from array import array
import sys
from os import listdir
from os.path import isfile, join
from datetime import datetime
import math
import numpy as np
ROOT.TH1.SetDefaultSumw2()
# fix time axis
start_time = ROOT.TTimeStamp(2018,7,21,0,0,0)
stop_time  = ROOT.TTimeStamp(2018,9,5,0,0,0)
# The time offset used in the POLA data is 1st of January 2007
t = ROOT.TTimeStamp(2007,1,1,0,0,0)
da = ROOT.TDatime(2007,1,1,0,0,0)
ROOT.gStyle.SetTimeOffset(da.Convert())

#######################################
#    FUNCTIONS
#######################################

def readfile(filename):
    data = np.loadtxt("tmp_dat/{}".format(filename), skiprows=1)
    x = array('d')
    y = array('d')
    for i in range(len(data)):
        x.append(data[i,0])
        y.append(data[i,1])
    return x, y

def plotTP(x_event, y_temp_in, y_temp_out, y_pressure, min, max, name, g):
    C = ROOT.TCanvas(name, name, 1200, 600)
    pad1 = ROOT.TPad("pad1","",0,0,1,1)
    pad3 = ROOT.TPad("pad3","",0,0,1,1)
    pad2 = ROOT.TPad("pad2","",0,0,1,1)
    pad1.SetGrid()
    pad2.SetGrid()
    pad3.SetGrid()
    pad2.SetFillStyle(4000); #will be transparent
    pad2.SetFrameFillStyle(0);
    pad3.SetFillStyle(4000); #will be transparent
    pad3.SetFrameFillStyle(0);

    pad1.Draw()
    pad1.cd()
    g_in_temp = ROOT.TGraph(len(x_event), x_event, y_temp_in)
    g_in_temp.SetTitle("POLA-0{} Temperature and Pressure [10 min time interval]".format(g))
    g_in_temp.SetLineColor(4)
    g_in_temp.SetLineWidth(2)
    g_in_temp.SetMinimum(min)
    g_in_temp.SetMaximum(max)
    g_in_temp.GetXaxis().SetTimeDisplay(1)
    g_in_temp.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_in_temp.GetXaxis().SetLabelOffset(0.03)
    g_in_temp.GetYaxis().SetTitle("Temperature [C]")
    g_in_temp.Draw("AL")


    pad2.Draw()
    pad2.cd()
    g_out_temp = ROOT.TGraph(len(x_event), x_event, y_temp_out)
    g_out_temp.SetTitle("")
    g_out_temp.SetLineColor(2)
    g_out_temp.SetLineWidth(2)
    g_out_temp.SetMinimum(min)
    g_out_temp.SetMaximum(max)
    g_out_temp.GetXaxis().SetTimeDisplay(1)
    g_out_temp.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_out_temp.GetXaxis().SetLabelOffset(0.03)
    g_out_temp.Draw("AL")

    pad3.Draw()
    pad3.cd()
    g_pressure = ROOT.TGraph(len(x_event), x_event, y_pressure)
    g_pressure.SetTitle("")
    g_pressure.SetLineColor(1)
    g_pressure.SetLineWidth(2)
    g_pressure.GetXaxis().SetTimeDisplay(1)
    g_pressure.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_pressure.GetXaxis().SetLabelOffset(0.03)
    g_pressure.GetYaxis().SetTitle("Pressure [mbar]")
    g_pressure.GetYaxis().SetLabelOffset(0.01)
    g_pressure.GetYaxis().SetTitleOffset(1.1);
    g_pressure.Draw("Y+AL")

    legend = ROOT.TLegend(0.12,0.75,0.4,0.85)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.AddEntry(g_in_temp,"Indoor Teperature","l")
    legend.AddEntry(g_out_temp,"Outdoor Temperature","l")
    legend.AddEntry(g_pressure,"Pressure","l")
    legend.Draw()
    C.Update()
    C.Print("../figures/POLA0{}_TP.pdf]".format(g))
    return C

def plotCoord(latitude, longitude, name, g):
    C = ROOT.TCanvas(name, name, 1200, 600)
    C.SetGrid()
    g_cord = ROOT.TGraph(len(longitude), longitude, latitude)
    g_cord.SetMarkerStyle(20)
    g_cord.SetMarkerColor(1)
    g_cord.SetLineColor(1)
    g_cord.SetLineWidth(2)
    g_cord.SetTitle("POLA-0{} Coordinates".format(g))
    g_cord.GetXaxis().SetTitle("Longitude")
    g_cord.GetYaxis().SetTitle("Latitude")
    g_cord.GetYaxis().SetLabelOffset(0.02)
    g_cord.GetYaxis().SetTitleOffset(1.4)
    g_cord.Draw("APL")
    C.Update()
    C.Print("../figures/POLA0{}_lat_long.pdf]".format(g))
    return C

def plotRawL(time, rawrate, L, name, g):
    C = ROOT.TCanvas(name, name, 1200, 600)
    pad1 = ROOT.TPad("pad1","",0,0,1,1)
    pad2 = ROOT.TPad("pad2","",0,0,1,1)
    pad1.SetGrid()
    pad2.SetFillStyle(4000); #will be transparent
    pad2.SetFrameFillStyle(0);

    pad1.Draw()
    pad1.cd()
    g_l = ROOT.TGraph(len(time), time, L)
    g_l.SetTitle("POLA-0{} {} and Rate over time [12 h time interval]".format(g,name))
    g_l.SetMarkerStyle(20)
    g_l.SetMarkerColor(4)
    g_l.SetLineColor(4)
    g_l.SetLineWidth(2)
    g_l.GetXaxis().SetTimeDisplay(1)
    g_l.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_l.GetXaxis().SetLabelOffset(0.03)
    g_l.GetYaxis().SetTitle("{}".format(name))
    g_l.Draw("APL")

    pad2.Draw()
    pad2.cd()
    g_raw = ROOT.TGraph(len(time), time, rawrate)
    g_raw.SetTitle("")
    g_raw.SetMarkerStyle(20)
    g_raw.SetMarkerColor(1)
    g_raw.SetLineColor(1)
    g_raw.SetLineWidth(2)
    g_raw.GetXaxis().SetTimeDisplay(1)
    g_raw.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_raw.GetXaxis().SetLabelOffset(0.03)
    g_raw.GetYaxis().SetTitle("Rate [Hz]")
    g_raw.GetYaxis().SetLabelOffset(0.01)
    g_raw.GetYaxis().SetTitleOffset(1.0);
    g_raw.Draw("Y+APL")

    legend = ROOT.TLegend(0.72,0.13,0.82,0.23)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.AddEntry(g_raw,"Rawrate","lp")
    legend.AddEntry(g_l, "{}".format(name), "lp")
    legend.Draw()
    C.Update()
    C.Print("../figures/POLA0{}_Raw_{}.pdf]".format(g, name))
    return C

def plotLTime(time, L, name):
    C = ROOT.TCanvas(name, name, 1200, 600)
    C.SetGrid()
    g_l = ROOT.TGraph(len(time), time, L)
    g_l.SetMarkerStyle(20)
    g_l.SetMarkerColor(1)
    #g_l.SetLineColor(1)
    #g_l.SetLineWidth(2)
    g_l.SetTitle("{} over time".format(name))
    g_l.GetYaxis().SetTitle("{}".format(name))
    g_l.GetXaxis().SetTimeDisplay(1)
    g_l.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_l.GetXaxis().SetLabelOffset(0.03)
    g_l.Draw("AP")
    C.Update()
    C.Print("../figures/POLA0{}_{}_time.pdf".format(g, name))
    return C

def plotLatLong(time, lat, long, name, g):
    C = ROOT.TCanvas(name, name, 1200, 600)
    pad1 = ROOT.TPad("pad1","",0,0,1,1)
    pad2 = ROOT.TPad("pad2","",0,0,1,1)
    pad1.SetGrid()
    pad2.SetFillStyle(4000); #will be transparent
    pad2.SetFrameFillStyle(0);

    pad1.Draw()
    pad1.cd()
    g_long = ROOT.TGraph(len(time), time, long)
    g_long.SetTitle("POLA-01 Latitude and Longitude over time [12 h time interval]")
    g_long.SetMarkerStyle(20)
    g_long.SetMarkerColor(4)
    g_long.SetLineColor(4)
    g_long.SetLineWidth(2)
    g_long.GetXaxis().SetTimeDisplay(1)
    g_long.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_long.GetXaxis().SetLabelOffset(0.03)
    g_long.GetYaxis().SetTitle("Longitude")
    g_long.Draw("APL")

    pad2.Draw()
    pad2.cd()
    g_lat = ROOT.TGraph(len(time), time, lat)
    g_lat.SetTitle("")
    g_lat.SetMarkerStyle(20)
    g_lat.SetMarkerColor(1)
    g_lat.SetLineColor(1)
    g_lat.SetLineWidth(2)
    g_lat.GetXaxis().SetTimeDisplay(1)
    g_lat.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_lat.GetXaxis().SetLabelOffset(0.03)
    g_lat.GetYaxis().SetTitle("Latitude")
    g_lat.GetYaxis().SetLabelOffset(0.01)
    g_lat.GetYaxis().SetTitleOffset(1.0);
    g_lat.Draw("Y+ALP")

    legend = ROOT.TLegend(0.72,0.13,0.82,0.23)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.AddEntry(g_lat,"Latitude")
    legend.AddEntry(g_long, "Longitude")
    legend.Draw()

    C.Update()
    C.Print("../figures/POLA0{}_lat_long_time.pdf]".format(g))
    return C

def plotRaw3(x1,x2,x3,y1,y2,y3,name, title):
    C = ROOT.TCanvas(name, name, 1200, 600)
    C.SetGrid()
    mg = ROOT.TMultiGraph("mg_{}".format(name),"mg_{}".format(name))

    g_RawRate1 = ROOT.TGraph(len(x1), x1, y1)
    g_RawRate1.SetMarkerStyle(20)
    g_RawRate1.SetMarkerColor(1)
    g_RawRate1.SetLineWidth(2)
    g_RawRate1.SetLineColor(1)
    g_RawRate1.SetTitle("POLA-01")

    g_RawRate2 = ROOT.TGraph(len(x2), x2, y2)
    g_RawRate2.SetMarkerStyle(20)
    g_RawRate2.SetMarkerColor(2)
    g_RawRate2.SetLineWidth(2)
    g_RawRate2.SetLineColor(2)
    g_RawRate2.SetTitle("POLA-02")

    g_RawRate3 = ROOT.TGraph(len(x3), x3, y3)
    g_RawRate3.SetMarkerStyle(20)
    g_RawRate3.SetMarkerColor(4)
    g_RawRate3.SetLineWidth(2)
    g_RawRate3.SetLineColor(4)
    g_RawRate3.SetTitle("POLA-03")

    mg.Add(g_RawRate1)
    mg.Add(g_RawRate2)
    mg.Add(g_RawRate3)
    mg.Draw("APL")
    mg.SetTitle("{} rate over time for all detectors [12 hour time interval]".format(title))
    mg.GetXaxis().SetTimeDisplay(1)
    mg.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    mg.GetXaxis().SetLabelOffset(0.03)
    mg.GetYaxis().SetTitle("Rate [Hz]")
    mg.GetYaxis().SetLabelOffset(0.01)
    mg.GetYaxis().SetTitleOffset(1.1);
    legend = C.BuildLegend(0.73,0.3,0.9,0.44)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    C.Update()
    C.Print("../figures/all_{}.pdf]".format(name))
    return C

def raw_pressure_fit(x_pres, y_raw, min, max, p_ref, alpha, name, g):
    #   Input: x_pres, y_raw, min, max, p_ref, name, g
    #   Output: C, corrected y_rawrate
    func = ROOT.TF1("func", "exp([0] + [1]*x)", 0, 10)
    C = ROOT.TCanvas(name, name, 1200, 600)
    C.SetGrid()
    g_raw = ROOT.TGraph(len(x_pres), x_pres, y_raw)
    g_raw.SetMarkerStyle(20)
    g_raw.SetMarkerColor(1)
    g_raw.SetLineColor(1)
    g_raw.SetLineWidth(2)
    g_raw.SetTitle("POLA-0{} Raw rate vs pressure".format(g))
    g_raw.GetYaxis().SetTitle("Rate [Hz]")
    g_raw.GetXaxis().SetTitle("Pressure [mbar]")
    g_raw.SetMinimum(min)
    g_raw.SetMaximum(max)
    g_raw.Draw("AP")
    fit = g_raw.Fit("func", "S")
    ROOT.gStyle.SetOptFit(111)
    legend = ROOT.TLegend(0.12,0.75,0.4,0.85)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.AddEntry(g_raw,"Raw rate")
    legend.AddEntry(func,"Exponential fit: f(x)=exp[p0 + p1 x]")
    legend.Draw()
    C.Update()
    #C.Draw()
    C.Print("../figures/POLA0{}_rate_pressure_fit.pdf]".format(g))
    b = fit.Get().Parameter(1)
    cor = array('d')
    for i in range(len(x_pres)):
        f = np.exp(alpha + b*(x_pres[i] - p_ref))
        n = f*y_raw[i]
        cor.append((f*y_raw[i]))
    return C, cor, b

def raw_temp_fit(x_temp, y_raw, min, max, name, g):
    #   Input: x_temp, y_raw, min, max, p_ref, name, g
    #   Output: C, corrected y_rawrate
    func = ROOT.TF1("func", "exp([0] + [1]*x)", 0, 10)
    C = ROOT.TCanvas(name, name, 1200, 600)
    C.SetGrid()
    g_tmp = ROOT.TGraph(len(x_temp), x_temp, y_raw)
    g_tmp.SetMarkerStyle(20)
    g_tmp.SetMarkerColor(1)
    g_tmp.SetLineColor(1)
    g_tmp.SetLineWidth(2)
    g_tmp.SetTitle("POLA-0{} Raw rate vs temperature".format(g))
    g_tmp.GetYaxis().SetTitle("Rate [Hz]")
    g_tmp.GetXaxis().SetTitle("Temperature [C]")
    g_tmp.SetMinimum(min)
    g_tmp.SetMaximum(max)
    g_tmp.Draw("AP")
    fit = g_tmp.Fit("func", "S")
    ROOT.gStyle.SetOptFit(111)
    #legend = C.BuildLegend()
    legend = ROOT.TLegend(0.12,0.75,0.4,0.85)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.AddEntry(g_tmp,"Raw rate")
    legend.AddEntry(func,"Exponential fit: f(x)=exp[p0 + p1 x]")
    legend.Draw()
    C.Update()
    #C.Draw()
    C.Print("../figures/POLA0{}_rate_temp_fit.pdf]".format(g))
    a = fit.Get().Parameter(0)
    b = fit.Get().Parameter(1)
    return C, b

def plotRaw1(xc, yc, x1, y1, alpha, beta, name, g):
        C = ROOT.TCanvas(name, name, 1200, 600)
        C.SetGrid()
        mg = ROOT.TMultiGraph("mg_{}".format(name),"mg_{}".format(name))

        g_RawRate2 = ROOT.TGraph(len(x1), x1, y1)
        g_RawRate2.SetMarkerStyle(20)
        g_RawRate2.SetMarkerColor(4)
        g_RawRate2.SetLineWidth(2)
        g_RawRate2.SetLineColor(4)
        g_RawRate2.SetTitle("Raw rate")

        g_RawRate1 = ROOT.TGraph(len(xc), xc, yc)
        g_RawRate1.SetMarkerStyle(20)
        g_RawRate1.SetMarkerColor(1)
        g_RawRate1.SetLineWidth(2)
        g_RawRate1.SetLineColor(1)
        g_RawRate1.SetTitle("Corrected rate")

        mg.Add(g_RawRate2)
        mg.Add(g_RawRate1)
        mg.Draw("APL")
        mg.SetTitle("POLA-0{} Rate, #alpha={:f} and #beta={:f}, [12 hour time interval]".format(g, alpha, beta))
        mg.GetXaxis().SetTimeDisplay(1)
        mg.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
        mg.GetXaxis().SetLabelOffset(0.03)
        mg.GetYaxis().SetTitle("Rate [Hz]")
        #mg.GetYaxis().SetLabelOffset(0.01)
        #mg.GetYaxis().SetTitleOffset(1.1);
        if g == 1:
            legend = C.BuildLegend(0.73,0.3,0.9,0.44)
        else:
            legend = C.BuildLegend(0.12,0.75,0.4,0.85)
        legend.SetFillStyle(0)
        legend.SetBorderSize(0)
        C.Update()
        C.Print("../figures/POLA0{}_corrected_rate.pdf]".format(g))
        return C

#######################################
#    Read data
#######################################

x1_rawrate, y1_rawrate = readfile("01_rawrate.txt")
x2_rawrate, y2_rawrate = readfile("02_rawrate.txt")
x3_rawrate, y3_rawrate = readfile("03_rawrate.txt")

x1_event, y1_press = readfile("01_event_pressure.txt")
x2_event, y2_press = readfile("02_event_pressure.txt")
x3_event, y3_press = readfile("03_event_pressure.txt")

y1_temp_inside, y1_temp_outside = readfile("01_temp.txt")
y2_temp_inside, y2_temp_outside = readfile("02_temp.txt")
y3_temp_inside, y3_temp_outside = readfile("03_temp.txt")

y1_long, y1_lat =  readfile("01_coordinates.txt")
y2_long, y2_lat =  readfile("02_coordinates.txt")
y3_long, y3_lat =  readfile("03_coordinates.txt")

x1_press, y1_rawrate1 = readfile("01_raw_press.txt")
x2_press, y2_rawrate1 = readfile("02_raw_press.txt")
x3_press, y3_rawrate1 = readfile("03_raw_press.txt")

x1_temp, y1_rawrate1 = readfile("01_raw_temp.txt")
x2_temp, y2_rawrate1 = readfile("02_raw_temp.txt")
x3_temp, y3_rawrate1 = readfile("03_raw_temp.txt")

#######################################
#    DO STUFF
#######################################

#   C = plotTP(x_event, y_temp_in, y_temp_out, y_pressure, min, max, name, g)
C11 = plotTP(x1_event, y1_temp_inside, y1_temp_outside, y1_press, 15, 35, "temp_pres1", 1)
C12 = plotTP(x2_event, y2_temp_inside, y2_temp_outside, y2_press, 23.5, 26, "temp_pres2", 2)
C13 = plotTP(x3_event, y3_temp_inside, y3_temp_outside, y3_press, 29, 38, "temp_pres3", 3)

# C = plotRaw3(x1,x2,x3,y1,y2,y3,name)
CA = plotRaw3(x1_rawrate,x2_rawrate,x3_rawrate,y1_rawrate,y2_rawrate,y3_rawrate, "raw3", "Raw")

#   C = plotCoord(latitude, longitude, name, g)
C21 = plotCoord(y1_lat, y1_long, "cord1", 1)


#   C = plotLatLong(time, lat, long, name, g)
C31 = plotLatLong(x1_rawrate, y1_lat, y1_long, "cord_time", 1)

#   C = plotRawL(time, rawrate, L, name)
C41 = plotRawL(x1_rawrate, y1_rawrate, y1_lat, "Latitude", 1)
C42 = plotRawL(x1_rawrate, y1_rawrate, y1_long, "Longitude", 1)

#   C1 = raw_temp_fit(x_temp, y_raw, min, max, p_ref, name, g)
C71, a1 = raw_temp_fit(x1_temp, y1_rawrate1, 5, 45, "tmp_fit", 1)
C72, a2 = raw_temp_fit(x2_temp, y2_rawrate1, 28, 38, "tmp_fit2", 2)
C73, a3 = raw_temp_fit(x3_temp, y3_rawrate1, 26, 29, "tmp_fit3", 3)

#   C = raw_pressure_fit(x_pres, y_raw, min, max, p_ref, alpha, name, g)
C51, y1_raw_cor,b1  = raw_pressure_fit(x1_press, y1_rawrate1, 5, 50, 1011.85, a1, "pr1", 1)
C52, y2_raw_cor,b2 = raw_pressure_fit(x2_press, y2_rawrate1, 30, 40, 1008.53, a2, "pr2", 2)
C53, y3_raw_cor,b3 = raw_pressure_fit(x3_press, y3_rawrate1, 27, 28.5, 985.87, a3, "pr3", 3)

#   C = plotRaw1(xc, yc, x1, y1, alpha, beta, name, g)
C61 = plotRaw1(x1_rawrate, y1_raw_cor, x1_rawrate, y1_rawrate1, a1, b1, "c_raw", 1)
C62 = plotRaw1(x2_rawrate, y2_raw_cor, x2_rawrate, y2_rawrate1, a2, b2,"c_raw2", 2)
C63 = plotRaw1(x3_rawrate, y3_raw_cor, x3_rawrate, y3_rawrate1, a3, b3,"c_raw3", 3)

#C = plotRaw3(x1,x2,x3,y1,y2,y3,name)
C9 = plotRaw3(x1_rawrate,x2_rawrate,x3_rawrate,y1_raw_cor,y2_raw_cor,y3_raw_cor,"corr3","Corrected")
