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
   string s = option.Data();
   string delimiter = "_";
   p_option = s.substr(0, s.find(delimiter)); // "data" or "mc"

   //Set counters to zero
   nEvents_tot = 0;
   nEvents1 = 0;
   nEvents2 = 0;
   nEvents3 = 0;
   nEvents4 = 0;
   nEvents5 = 0;

   //Define histograms
   hist_mass_all = new TH1F("hist_mass_all","hist_mass_all", 30, 105, 160.);
   hist_mass_unconv = new TH1F("hist_mass_unconv","hist_mass_unconv", 30, 105, 160.);
}

void analysis::SlaveBegin(TTree * /*tree*/)
{
   // The SlaveBegin() function is called after the Begin() function.
   // When running with PROOF SlaveBegin() is called on each slave server.
   // The tree argument is deprecated (on PROOF 0 is passed).

   TString option = GetOption();
   cout << "------------------------------------------"<< endl;
   cout << "Processing dataset:  " << option << endl;
   cout << "------------------------------------------"<< endl;

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
   //

   fReader.SetLocalEntry(entry);
   TString option = GetOption();

   //Count total number of events.
   nEvents_tot++;

   // Set scale factors
   Float_t scaleFactor = 1.0;

   if(p_option == "mc"){
      scaleFactor = (*mcWeight)*(*scaleFactor_PILEUP)*(*scaleFactor_PHOTON)*(*scaleFactor_PhotonTRIGGER);
   }

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
       dPhi = dPhi < TMath::Pi() ? dPhi : 2*TMath::Pi() - dPhi;

       float mass = sqrt(2*photon1.Pt()*photon2.Pt()*(cosh(dEta) - cos(dPhi)));

       // Kinematic selection requires ET/m >0.35 for leading and 0.25 for subleading
       if (!(photon1.E()/mass > 0.35 && photon2.E()/mass > 0.25)){return kTRUE;}
       nEvents4++;

       // Cut on known mass window
       if(!(mass > 105. && mass < 160.)){return kTRUE;}
       nEvents5++;

       //fill histograms
       hist_mass_all->Fill(mass, scaleFactor);

       if (photon_convType[0] == 0 && photon_convType[1] == 0) {
          /* only the unconverted ones*/
          hist_mass_unconv->Fill(mass, scaleFactor);
       }


    } // End of trigP
   return kTRUE;
}

void analysis::SlaveTerminate()
{
   // The SlaveTerminate() function is called after all entries or objects
   // have been processed. When running with PROOF SlaveTerminate() is called
   // on each slave server.
}

void analysis::Terminate()
{
   // The Terminate() function is the last function to be called during
   // a query. It always runs on the client, it can be used to present
   // the results graphically or save the results to file.

   cout << "Total number of events prosessed:   " << nEvents_tot << endl;
   cout << "Number of events after cuts:        " << nEvents5 << endl;
   cout << "" <<endl;
   TString option = GetOption();
   write_histogram(hist_mass_all, hist_mass_unconv, p_option, option);
   //write_histogram(hist_mass_unconv, p_option, option);

}


void analysis::write_histogram(TH1F *hist1, TH1F *hist2, string folder, TString option){
   TString indir = "output/"+folder+"/";
   TString filename = "outfile."+option+".root";
   TFile file(indir+filename, "RECREATE");
   hist1->Write();
   hist2->Write();
   file.Close();
   cout << "histograms saved in:  " << indir+filename << endl;
   hist1->Reset();
   hist2->Reset();
}
