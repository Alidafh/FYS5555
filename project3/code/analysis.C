#define analysis_cxx
// The class definition in analysis.h has been generated automatically
// by the ROOT utility TTree::MakeSelector(). This class is derived
// from the ROOT class TSelector. For more information on the TSelector
// framework see $ROOTSYS/README/README.SELECTOR or the ROOT User Manual.


// The following methods are defined in this file:
//    Begin():        called every time a loop on the tree starts,
//                    a convenient place to create your histograms.
//    SlaveBegin():   called after Begin(), when on PROOF called only on the
//                    slave servers.
//    Process():      called for each event, in this function you decide what
//                    to read and fill your histograms.
//    SlaveTerminate: called at the end of the loop on the tree, when on PROOF
//                    called only on the slave servers.
//    Terminate():    called at the end of the loop on the tree,
//                    a convenient place to draw/fit your histograms.
//
// To use this file, try the following session on your Tree T:
//
// root> T->Process("analysis.C")
// root> T->Process("analysis.C","some options")
// root> T->Process("analysis.C+")
//


#include "analysis.h"
#include "analysis_histograms.h"
#include <TH2.h>
#include <TStyle.h>
#include <TH1.h>
#include <TMath.h>

#include <TLorentzVector.h>
#include <TCanvas.h>

#include <iostream>
#include <math.h>
using namespace std;


void analysis::Begin(TTree * /*tree*/)
{
   // The Begin() function is called at the start of the query.
   // When running with PROOF Begin() is only called on the client.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();

   nEvents_tot = 0;
   nEvents1 = 0;
   nEvents2 = 0;
   nEvents3 = 0;
   nEvents4 = 0;
   nEvents5 = 0;
   //Define histograms
   hist_mass_bin1 = new TH1F("hist_mYY_bin1","hist_mYY_bin1", 30, 105, 160.);
   hist_mass_bin1->GetXaxis()->SetTitle(" mass [GeV]");
   hist_mass_bin1->GetYaxis()->SetTitle("number of events");

}

void analysis::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   printf("Starting analysis with process option: %s \n", option.Data());

}

Bool_t analysis::Process(Long64_t entry)
{
   // The Process() function is called for each entry in the tree (or possibly
   // keyed object in the case of PROOF) to be processed. The entry argument
   // specifies which entry in the currently loaded tree is to be processed.
   // When processing keyed objects with PROOF, the object is already loaded
   // and is available via the fObject pointer.
   //
   // This function should contain the \"body\" of the analysis. It can contain
   // simple or elaborate selection criteria, run algorithms on the data
   // of the event and typically fill histograms.
   //
   // The processing can be stopped by calling Abort().
   //
   // Use fStatus to set the return value of TTree::Process().
   //
   // The return value is currently not used.

   fReader.SetLocalEntry(entry);

   nEvents_tot++;
   if( nEvents_tot % 1000000 == 0 ){cout << nEvents_tot/1E6 << " million events processed" << endl;}


   // Boolean whether event passes a diphoton trigger, ie. at least two photons in event
   if (*trigP) {
       nEvents1++;

       // Exactly two photons
       if (!(*photon_n == 2)){return kTRUE;}
       nEvents2++;


       for (unsigned  int i = 0; i < *photon_n; i++) {
          /*  Event preselection: The photon candidates in the event must have
               ET > 25 GeV and |eta| < 2.37 (1.37<|eta|<1.52).
               Also check if photon is tight and isolated */
          if(!(photon_E[i]/1000 > 25.0)){return kTRUE;}
          if(!(abs(photon_eta[i]) < 2.37)){return kTRUE;}
          if(!(abs(photon_eta[i]) > 1.37 || abs(photon_eta[i]) < 1.52)){return kTRUE;}
          if(!(photon_isTightID->at(i) == true)){return kTRUE;}
          if(!(photon_ptcone30[i]/photon_pt[i] < 0.065 && photon_etcone20[i]/photon_pt[i] < 0.065)){return kTRUE;}
       }

       nEvents3++;

       // create lorentz vectors
       TLorentzVector photon1 = TLorentzVector();
       TLorentzVector photon2 = TLorentzVector();

       // fill lorentz vectors, divide by 1000 to get values in GeV
       photon1.SetPtEtaPhiE(photon_pt[0]/1000., photon_eta[0], photon_phi[0], photon_E[0]/1000.);
       photon2.SetPtEtaPhiE(photon_pt[1]/1000., photon_eta[1], photon_phi[1], photon_E[1]/1000.);

       if(photon_pt[1]>photon_pt[0]){
          /* sort lorentz vectors so that photon1 is leading and photon2 is subleading */
          photon1.SetPtEtaPhiE(photon_pt[0]/1000., photon_eta[0], photon_phi[0], photon_E[0]/1000.);
          photon2.SetPtEtaPhiE(photon_pt[1]/1000., photon_eta[1], photon_phi[1], photon_E[1]/1000.);
       }

       // calculate the invariant mass
       float dEta = photon1.Eta() - photon2.Eta();
       float dPhi = photon1.Phi() - photon2.Phi();
       float mass = sqrt(2*photon1.Pt()*photon2.Pt()*(cosh(dEta) - cos(dPhi)));

       // Kinematic selection requires ET/m >0.35 for leading and 0.25 for subleading
       if (!(photon1.E()/mass > 0.35 && photon2.E()/mass > 0.25)){return kTRUE;}
       nEvents4++;

       // Cut on known mass window
       if(!(mass > 105. && mass < 160.)){return kTRUE;}
       nEvents5++;

       //fill histogram and write to file
       hist_mass_bin1->Fill(mass);

    } // End of trigP
   return kTRUE;
}

void analysis::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.
   cout << "SlaveTerminate: YOU HAVE NOT WRITTEN THIS PART OF THE CODE YET!!"<<endl;
}

void analysis::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.
   cout << "number of events prosessed:   " << nEvents_tot << endl;
   cout << "nEvents1= " << nEvents1 << endl;
   cout << "nEvents2=  " << nEvents2 << endl;
   cout << "nEvents3=  " << nEvents3 << endl;
   cout << "nEvents4=  " << nEvents4 << endl;
   cout << "nEvents5=  " << nEvents5 << endl;
   TString option = GetOption();
   make_histogram_file(hist_mass_bin1, "test", option);
   //c1 = new TCanvas("c1","c1",800,1000);
   //hist_mass_bin1->Draw("P*");
   //c1->Draw();
}
