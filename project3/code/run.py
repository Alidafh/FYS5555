import ROOT as ro
import sys, os, time
import re

def run_analysis(arg, indir):
    """
    Executes analysis.C on the chosen dataset.
    input:
        arg - either "Data" or "MC"
        indir - directory where the datasets are saved(path is entered below)
    """
    # Begin timer
    t0 = time.time()
    myChain = ro.TChain('mini')
    arglist = []
    print ('-------------------------------------------')
    if arg == 'Data':
        print('Running on real data located in: {}'.format(indir))
    elif arg =='MC':
        print('Running on Monte Carlo located in: {}'.format(indir))
    for filename in os.listdir(indir):
        if not '.root' in filename: continue
        print (filename)
#        arglist.append(re.findall(r"^.*?(?=G)", filename))
        myChain.Add(indir+'/'+filename)

#    print ("\n",arglist)
    entries = myChain.GetEntries()
    print ('\nNumber of events to process: {:d}\n'.format(entries))
    print ('-------------------------------------------')
    myChain.Process('analysis.C+', arg)
    t = int( time.time()-t0 )/60
    print ('Time spent: {:f} min'.format(t))



if __name__ == '__main__':

    # Add your path to files here
    my_path = '/home/alida/Documents/uio/Master/FYS5555/project3/GamGam/'

    while True:
        try:
            type = int(input('0-run on data\n1-run on MC\n2-run on both\n'))
            break
        except:
            print('Choose a number!\n')

    # Create the folders for histograms
    while True:
        try:
            os.makedirs('./output/datafiles', exist_ok=False)
            os.makedirs('./output/plots', exist_ok=False)
            break
        except:
            answer = input('\ndirectory /output already exists, continue with this folder [y/n]  ')
            if answer == 'y':
                os.makedirs('./output/datafiles', exist_ok=True)
                os.makedirs('./output/plots', exist_ok=True)
                #print('Files will be saved in folder: /output \n')
                break
            else:
                quit()


    # Run analysis depending on type of input option
    if type == 0:
            #print('mode: Data\n')
            arg1 = 'Data'
            input_dir = my_path+arg1
            run_analysis(arg1,input_dir)
    elif type == 1:
            #print('mode: Monte Carlo\n')
            arg1 = 'MC'
            input_dir = my_path+arg1
            run_analysis(arg1, input_dir)
    elif type==2:
            #print('mode: Both data and MC\n')
            arg1 = ['Data', 'MC']
            input_dir = [my_path+arg1[0], my_path+arg1[1]]
            for i in range(len(arg1)):
                run_analysis(arg1[i] , input_dir[i])


'''
def func2(dat, indir):
    for filename in os.listdir(indir):
            if not '.root' in filename: continue
            print (filename)
            myChain.Add(input_dir+'/'+filename)
    if arg1 == 'MC':
            for filename in os.listdir(input_dir):
                if not '.root' in filename: continue
                print (filename)
                myChain.Add(input_dir+'/'+filename)
'''
