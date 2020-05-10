import os
import ROOT as ro
from run import run_analysis

my_path = '/home/alida/Documents/uio/Master/FYS5555/project3/temp'
arg = 'Data'
filename = "data_A.GamGam.root"
myChain = ro.TChain('mini')
myChain.Add(my_path+'/'+filename)
myChain.Process('analysis.C+', arg)
