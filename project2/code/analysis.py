import ROOT
from array import array
import sys
from os import listdir
from os.path import isfile, join
from datetime import datetime
import math
ROOT.TH1.SetDefaultSumw2()

# Function to retrieve difference in seconds between two time stamps
def getDuration(start,stop):
    timestamp_start = "%d %06d" %(t.GetDate(True,start),t.GetTime(True,start))
    timestamp_stop  = "%d %06d" %(t.GetDate(True,stop),t.GetTime(True,stop))

    datetime_object_start = datetime.strptime(timestamp_start, '%Y%m%d %H%M%S')
    datetime_object_stop  = datetime.strptime(timestamp_stop,  '%Y%m%d %H%M%S')
    difference = datetime_object_stop - datetime_object_start
    seconds_in_day = 24 * 60 * 60
    if difference.days < 0:
        return difference.seconds
    else:
        return difference.days * seconds_in_day + difference.seconds


# Folder where the data is stored
while True:
    g = input("Specify detector (1: POLA-01, 2: POLA-02, 3: POLA-03):  ")
    try:
        dataset = int(g)
        break
    except:
        print ("Please specify an integer in [1-3]")

indir = "/home/alida/Documents/uio/FYS5555/project2/data/POLA-0{}".format(g)

# The three trees containing different data
c_trend = ROOT.TChain("Trending")
c_headr = ROOT.TChain("Header")
c_weath = ROOT.TChain("Weather")

# Define time span (default: defined as the expedition with Nanuq (PolarquEEEst)
start_time = ROOT.TTimeStamp(2018,7,21,0,0,0)
stop_time  = ROOT.TTimeStamp(2018,9,5,0,0,0)

# Loop over files in input directory and select those
# which are inside the time span defined above
onlyfiles = [f for f in listdir(indir) if isfile(join(indir, f))]
print ("Found {} files in folder {}".format(len(onlyfiles), indir))

files_to_use = []
for fname in sorted(onlyfiles):
    #skip files tat do not have ending summary.root
    if not fname.endswith("summary.root"): continue

    # Get start date and stop date from file name
    st_y, st_m, st_d = (fname.split("_")[1]).split("-")
    start_dt = ROOT.TTimeStamp(int(st_y),int(st_m),int(st_d),0,0,0).AsDouble()
    en_y,en_m,en_d = (fname.split("_")[2]).split("-")
    stop_dt  = ROOT.TTimeStamp(int(en_y),int(en_m),int(en_d),0,0,0).AsDouble()

    # check if within the specified time period
    if start_dt > start_time.AsDouble() and stop_dt < stop_time.AsDouble():
        files_to_use.append(join(indir,fname))

# Print summary and add files to TChains
print ("INFO \t Found {} files in wanted time span from {} to {}".format(len(files_to_use),start_time.AsString("s"),stop_time.AsString("s")))
for ftu in files_to_use:
    c_trend.Add(ftu)
    c_headr.Add(ftu)
    c_weath.Add(ftu)


# The time offset used in the POLA data is 1st of January 2007
t = ROOT.TTimeStamp(2007,1,1,0,0,0)
da = ROOT.TDatime(2007,1,1,0,0,0)
ROOT.gStyle.SetTimeOffset(da.Convert());

# Get the number of entries
nentries_headr = c_headr.GetEntries()
nentries_weath = c_weath.GetEntries()
nentries_trend = c_trend.GetEntries()

print ("Number of runs   :", nentries_headr)
print ("Number of events :", nentries_trend)

if nentries_headr != nentries_weath:
    sys.exit("ERROR \t Number of events in header and weather do not match!. Exiting")


####################################
# Define histograms and arrays
####################################
x_rawrate = array('d')
y_rawrate = array('d')
x_pres_w = array('d')

x_event = array('d')
y_pressure = array('d')
y_temp_in = array('d')
y_temp_out = array('d')
x_temp = array('d')

y_lat = array('d')
y_long = array('d')
x_time_coord = array('d')

h_indoor_temp = ROOT.TH1F("h_indoor_temp","",60,0,60)
h_outdoor_temp = ROOT.TH1F("h_outdoor_temp", "", 60, 0 ,60)
h_time_temp = ROOT.TH1F("h_time_temp","",60,0,60)
h_err_temp = ROOT.TH1F("h_err_temp","",60,0,60)

h_nev_pressure = ROOT.TH1F("h_nev_pressure","",1500,0,1500)
h_time_pressure = ROOT.TH1F("h_time_pressure","",1500,0,1500)
h_err_pressure = ROOT.TH1F("h_err_pressure","",1500,0,1500)

h_latitude = ROOT.TH1F("h_latitude", "", 1500, 0 ,90)
h_longitude = ROOT.TH1F("h_longitude", "", 1500, -180, 180)

####################################
"""
c_weath.GetEntry(0)
h_indoor_temp.Fill(c_weath.IndoorTemperature)

print (c_weath.IndoorTemperature)
"""

vb = 0  # Set vb to non-zero value if you want some extra print-out
storeStartTime_run = True
tot_numevents = 0.0
tot_duration = 0

# Loop over runs
for i in range(nentries_headr):
    if i%100 == 0: print ("Run {}/{}".format(i,nentries_headr))

    # Get entry i from TTrees (important!)
    c_headr.GetEntry(i)
    c_weath.GetEntry(i)

    # Exclude runs with few events
    if c_headr.NumEvents < 12000: continue

    # Get duration, start and end time for run (in seconds from 1/1/2007)
    start = int(c_headr.RunStart)
    stop  = int(c_headr.RunStop)

    run_duration  = getDuration(start,stop)

    # Some runs seem to have some bad start and stop values, exclude those
    if run_duration > 1000000:
        print ("skipping", fname)
        continue
    # Skip short runs (less than 10 minutes)
    if (run_duration/60.) < 10: continue

    # store start of time bin
    if storeStartTime_run:
        start_new_block = start
        storeStartTime_run = False

    if vb > 0:
        print ("Run duration =", (run_duration))
        print ("Start: {} {}".format(t.GetDate(True,start),t.GetTime(True,start)))
        print ("Stop : {} {}".format(t.GetDate(True,stop),t.GetTime(True,stop)))

    # Accumulate number of events and time
    tot_duration  += run_duration
    tot_numevents += c_headr.NumEvents

    # If reached the wanted time span for adding a new point (default: 12 hours)
    if tot_duration >= 12.*60.*60.:
        # Fill x-values with the time (in seconds) in the middle of the range
        x_rawrate.append((start_new_block+(tot_duration/2.)))
        # Fill the raw rate in y-value
        y_rawrate.append(tot_numevents/tot_duration)
        y_long.append(c_headr.longitude)
        y_lat.append(c_headr.latitude)
        x_pres_w.append(c_weath.Pressure)
        x_temp.append(c_weath.IndoorTemperature)
        # reset variables
        tot_duration = 0.0
        tot_numevents = 0.0

        storeStartTime_run = True

    # Fill histograms for every event
    h_outdoor_temp.Fill(c_weath.OutdoorTemperature, c_headr.NumEvents)
    h_indoor_temp.Fill(c_weath.IndoorTemperature, c_headr.NumEvents)
    h_time_temp.Fill(c_weath.IndoorTemperature, run_duration)

    # fill arrays for longitude/latitide
    #y_long.append(c_headr.longitude)
    #y_lat.append(c_headr.latitude)
    #x_time_coord.append((start_new_block+(tot_duration/2.)))
    # This histogram is needed to get the proper statistical uncertainty
    # (i.e. same histograms as above, but storing the number of entries, N)
    # Error is given by sqrt(N)
    h_err_temp.Fill(c_weath.IndoorTemperature)


# Loop over all the events in this run
tot_duration_ev = 0
tot_intemp_ev = 0.0
tot_outtemp_ev = 0.0
tot_pressure_ev = 0.0
nev_in_block = 0
storeStartTime_ev = True
for j in range(nentries_trend):
    c_trend.GetEntry(j)

    if j%1000 == 0: print ("Event {}/{}".format(j,nentries_trend))

    # Start and stop time of events
    ev_start = int(c_trend.BinStart)
    ev_stop  = int(c_trend.BinEnd)

    # If start of a new time interval
    if storeStartTime_ev:
        ev_start_block = ev_start
        storeStartTime_ev = False

    # Get length of run (in seconds)
    ev_duration = getDuration(ev_start,ev_stop)

    # Some runs seem to have invalid start/stop times
    # Exclude those which are outside the time range defined at the beginning of the program
    # (i.e. the time of the PolarquEEEst experiment)
    if ev_stop > stop_time.AsDouble():
        continue
    # Skip short runs
    if ev_duration > 61: continue

    tot_duration_ev  += ev_duration
    tot_intemp_ev    += c_trend.IndoorTemperature
    tot_outtemp_ev   += c_trend.OutdoorTemperature
    tot_pressure_ev  += c_trend.Pressure
    nev_in_block += 1

    # If total duration is larger then the chosen time interval (default: 10 min)
    if tot_duration_ev >= 10.*60.:
        if vb > 0:
            print ("Tot duration for data period ", (tot_duration_ev/(60.)))

        # Fill x-axis (time in middle of interval)
        x_event.append((ev_start_block+(tot_duration_ev/2.)))

        # Fill y-values (temperature, pressure)
        y_pressure.append(tot_pressure_ev/nev_in_block)
        y_temp_in.append(tot_intemp_ev/nev_in_block)
        y_temp_out.append(tot_outtemp_ev/nev_in_block)

        # Reset counters
        storeStartTime_ev = True
        tot_duration_ev = 0.0
        tot_intemp_ev = 0.0
        tot_outtemp_ev = 0.0
        tot_pressure_ev = 0.0
        nev_in_block = 0


def write_data(filename, x, y, x_name, y_name):
    file = open("tmp_dat/0{}_{}.txt".format(g,filename), "w")
    file.write("{}  {}\r\n".format(x_name, y_name))
    if len(x)>len(y):
        n = len(x)
    else:
        n=len(y)
    for i in range(n):
        file.write("{}  {} \r\n".format(x[i], y[i]))
    file.close()
    print("Data saved in tmp_dat/0{}_{}.txt".format(g, filename))


#write_data("temp", y_temp_in, y_temp_out, "y_temp_in", "y_temp_out")
#write_data("event_pressure", x_event, y_pressure, "x_event", "y_pressure")
#write_data("rawrate", x_rawrate, y_rawrate, "x_rawrate", "y_rawrate")
#write_data("coordinates", y_long, y_lat, "y_long", "y_lat")
#write_data("raw_press", x_pres_w, y_rawrate, "x_pres_w", "y_rawrate")
write_data("raw_temp", x_temp, y_rawrate, "x_temp", "y_rawrate")

#################
#   Plotting
#################


def plotTP(min, max, name):
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
    g_in_temp.SetTitle("POLA-0{} [10 min time interval]".format(g))
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
    g_out_temp.SetTitle("POLA-0{} [10 min time interval]".format(g))
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
    g_pressure.SetTitle("POLA-0{} [10 min time interval]".format(g))
    g_pressure.SetLineColor(1)
    g_pressure.SetLineWidth(2)
    g_pressure.GetXaxis().SetTimeDisplay(1)
    g_pressure.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
    g_pressure.GetXaxis().SetLabelOffset(0.03)
    g_pressure.GetYaxis().SetTitle("Pressure [hPa]")
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
    #C.Print("../figures/POLA0{}_TP.pdf]".format(g))
    return C

def plotCoord(latitude, longitude, name):
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

def plotRawL(time, rawrate, L, name):
    C = ROOT.TCanvas(name, name, 1200, 600)
    pad1 = ROOT.TPad("pad1","",0,0,1,1)
    pad2 = ROOT.TPad("pad2","",0,0,1,1)
    pad1.SetGrid()
    pad2.SetFillStyle(4000); #will be transparent
    pad2.SetFrameFillStyle(0);

    pad1.Draw()
    pad1.cd()
    g_l = ROOT.TGraph(len(time), time, L)
    g_l.SetTitle("POLA-01 {} and Raw Rate over time [12 h time interval]".format(name))
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
    #C.Print("../figures/POLA0{}_{}_time.pdf".format(g, name))
    return C

def plotLatLong(time, lat, long, name):
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


#C3 = plotCoord(y_lat, y_long, "coord")
#C4 = plotRawL(x_rawrate, y_rawrate, y_lat, "Latitude")
#C5 = plotRawL(x_rawrate, y_rawrate, y_long, "Longitude")
#C6 = plotLatLong(x_rawrate, y_lat, y_long, "latlong")

"""
C3 = ROOT.TCanvas("c3", "c3", 1200, 600)
g_out_temp = ROOT.TGraph(len(x_event), x_event, y_temp_out)
g_in_temp = ROOT.TGraph(len(x_event), x_event, y_temp_in)
g_pressure = ROOT.TGraph(len(x_event), x_event, y_pressure)
g_out_temp.SetMarkerStyle(20)
g_out_temp.SetTitle("POLA-0{} Outdoor Temperature".format(g))
g_out_temp.GetXaxis().SetTimeDisplay(1)
g_out_temp.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
g_out_temp.GetXaxis().SetLabelOffset(0.03)
g_out_temp.Draw("AP")
C3.Draw()

C = ROOT.TCanvas("c", "c", 1200, 600)
g_RawRate = ROOT.TGraph(len(x_rawrate),x_rawrate,y_rawrate)
# The default marker in ROOT is horrible so let's change
g_RawRate.SetMarkerStyle(20)
# Get x-axis in date and time instead of seconds since 2007
g_RawRate.GetXaxis().SetTimeDisplay(1)
# Format the axis (default is date and time split in two lines)
g_RawRate.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
g_RawRate.GetXaxis().SetLabelOffset(0.03)
# Draw with axis and points
g_RawRate.Draw("AP")
C.Draw()


C1 = ROOT.TCanvas("c1", "c1", 1200, 600)
g_pressure = ROOT.TGraph(len(x_event), x_event, y_pressure)
g_pressure.SetMarkerStyle(20)
g_pressure.SetTitle("POLA-0{} Pressure".format(g))
g_pressure.GetXaxis().SetTimeDisplay(1)
g_pressure.GetXaxis().SetTimeFormat("#splitline{%d/%m/%y}{%H:%M}");
g_pressure.GetXaxis().SetLabelOffset(0.03)
g_pressure.Draw("AP")
C1.Draw()


C3 = ROOT.TCanvas("c3", "c3", 1200, 600)
h_indoor_temp = h_indoor_temp.Clone("h_indoor_temp")
h_indoor_temp.SetMarkerStyle(20)
h_indoor_temp.SetTitle("POLA-0{} Indoor Temperature? ".format(g))
# Set the errors correctly
for i in range(1,h_indoor_temp.GetNbinsX()+1):
    h_indoor_temp.SetBinError(i,h_err_temp.GetBinError(i))
    h_time_temp.SetBinError(i,h_err_temp.GetBinError(i))
h_indoor_temp.Divide(h_indoor_temp,h_time_temp)
h_indoor_temp.Draw("e")
C3.Draw()
"""
