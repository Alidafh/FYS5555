
#include "TROOT.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include <iostream>


void make_histogram_file(TH1F *hist , TString s, TString s1){
   TString indir = "output/datafiles/";
   TString filename = "outfile_"+s+"_"+s1+".root";
   TFile file(indir+filename, "RECREATE");
   hist->Write();
   file.Close();
   cout << "histogram saved:  " << indir+filename << endl;
}
