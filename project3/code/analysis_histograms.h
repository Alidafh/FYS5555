
#include "TROOT.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include <iostream>


void output_histogram_file(TH1F *hist , TString s, TString option){
   TString indir = "output/datafiles/";
   TString filename = "outfile."+option+"."+s+".root";
   TFile file(indir+filename, "RECREATE");
   hist->Write();
   file.Close();
   cout << "histogram saved:  " << indir+filename << endl;
   hist->Reset();
}

void fill_histogram(TH1F *hist, Double_t mass, Double_t weight){
   hist->Fill(mass, weight);
}
