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


4) plotting TBD
   - neet to fix statistics for histograms.
