# FYS5555 - Project 3

How to use:

1) Download the Gamma Gamma data from the CERN Open Data portal:
   http://opendata.cern.ch/record/15006

2) Open the python script 'run_analysis.py'
   - update the path in 'my_path' to the location of your data.
   - my_path = 'path/to/data/GamGam/'

3) Run the analysis script 'run_analysis.sh'
   - source run_analysis.sh or ./run_analysis.sh

   - You will be asked if you want to run on real data[0], only monte carlo[1],
      or running for both[2]. Choosing both may take some time.

   - New folders called 'output/data', 'output/mc' and 'output/figures'
     will be created. If these already exists, the existing folders will be used.


4) There are two plotting programs: 'plot_histograms.py' and 'plot_div.py'.  

   - To run both of these, do:

      source plot.sh

    Figures are saved in output/figures where files named "CP1_*" are for the
    inclusive categody and so on.

   1. 'plot_histograms.py' analyses the invariant mass distribution, doing
      signal, signal+background and background only modeling. The figures are
      saved in the folder output/figures. The category needs to be specified on
      the command line:

      python plot_histograms.py [number]

     where [number] = 0,1,2,3 for cp1,cp2,cp3,cp4 respectively.

   2. 'plot_div.py' plots the kinematic variables for the inclusive category(cp1)
      after all cuts. Figures are saved in the folder output/figures To run this simply do:

      python plot_div.py
