
#include "TROOT.h"
#include "TH1.h"
#include "TH2.h"
#include "TH3.h"
#include <iostream>


void output_histogram_file(TH1F *hist , string folder, TString option){
   //TString indir = "output/datafiles/";
   TString indir = "output/"+folder+"/";
   TString filename = "outfile."+option+".root";
   TFile file(indir+filename, "UPDATE");
   hist->Write();
   file.Close();
   cout << "histogram saved:  " << indir+filename << endl;
   hist->Reset();
}

void fill_histogram(TH1F *hist, Double_t mass, Double_t weight){
   hist->Fill(mass, weight);
}
