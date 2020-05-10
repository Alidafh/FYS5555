#include <TH2.h>
#include <TStyle.h>
#include <TH1.h>
#include <TMath.h>

#include <TLorentzVector.h>
#include <TCanvas.h>

#include <iostream>
#include <math.h>
using namespace std;

void test(){
TFile *f = new TFile("output/datafiles/outfile_test_Data.root");
TH1F *hist_mass_bin1 = new TH1F("h","h title", 100, 0, 4);
hist_mass_bin1 = (TH1F*)f->Get("hist_mYY_bin1");
hist_mass_bin1->SetTitle("Higgs");
TCanvas *c1 = new TCanvas("c1","c1",1000,600);

hist_mass_bin1->Draw("P*");

// The functional form to model the background distribution is chosen to be a third-order polynomial restricted to 105 < m(yy) < 160 GeV
TF1 *fit = new TF1("fit", "([0]+[1]*x+[2]*x^2+[3]*x^3)+[4]*exp(-0.5*((x-[5])/[6])^2)", 105, 160);
fit->FixParameter(5,125.0); // always fixed to 125 GeV

hist_mass_bin1->Fit("fit");
c1->Draw();


//f->Close();
}
