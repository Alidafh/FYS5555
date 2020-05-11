#!/bin/bash

echo "0 - Data"
echo "1 - MC"
echo "2 - Both"

read type

if [ $type -eq 0 ]
then
   echo "Analysis on real data started..."
   python run_analysis.py 0 $type
   python run_analysis.py 1 $type
   python run_analysis.py 2 $type
   python run_analysis.py 3 $type
fi

if [ $type -eq 1 ]
then
   echo "Analysis on Monte Carlo simulations started..."
   python run_analysis.py 0 $type
   python run_analysis.py 1 $type
   python run_analysis.py 2 $type
   python run_analysis.py 3 $type
   python run_analysis.py 4 $type
fi

if [ $type -eq 2 ]
then
   echo "Analysis on both Data and Monte Carlo started..."
   echo "this may take some time, you should go get some coffee while you wait.."
   python run_analysis.py 0 0
   python run_analysis.py 1 0
   python run_analysis.py 2 0
   python run_analysis.py 3 0
   python run_analysis.py 0 1
   python run_analysis.py 1 1
   python run_analysis.py 2 1
   python run_analysis.py 3 1
   python run_analysis.py 4 1
fi

pkill -f run_analysis.py
