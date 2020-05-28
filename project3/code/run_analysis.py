import ROOT as ro
import sys, os
import re

def Quiet(func,level = ro.kInfo + 1):
    def qfunc(*args,**kwargs):
        oldlevel = ro.gErrorIgnoreLevel
        ro.gErrorIgnoreLevel = level
        try:
            return func(*args,**kwargs)
        finally:
            ro.gErrorIgnoreLevel = oldlevel
    return qfunc

def run_process(indir, filename, i):
    if i ==0: #Data
        arg = re.match("^.*?(?=.G)", filename)[0]
    elif i==1: #MC
        arg = re.match("^.*?(?=_gam)", filename)[0]
    myChain = ro.TChain('mini')
    myChain.Add(indir+filename)
    myChain.Process('analysis.C',arg)

def get_filenames(indir):
    filenames = []
    for filename in os.listdir(indir):
        if not '.root' in filename: continue
        filenames.append(filename)
    return filenames


if __name__ == '__main__':
    num = int(sys.argv[1])
    type = int(sys.argv[2])

    # Add your path to files here
    my_path = '/home/alida/Documents/uio/Master/FYS5555/project3/GamGam/'
    folder = ["Data/" if type==0 else "MC/"][0]
    indir = my_path+folder
    files = get_filenames(indir)

    run_process(indir, files[num], type)
