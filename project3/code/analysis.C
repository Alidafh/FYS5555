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
   nEvents6 = 0;

   //Define histograms
   hist_mass_CP2 = new TH1F("hist_mass_CP2","hist_mass_CP2 ;m_{#gamma#gamma}; Events", 30, 105, 160.);
   hist_mass_CP3 = new TH1F("hist_mass_CP3","hist_mass_CP3 ;m_{#gamma#gamma}; Events", 30, 105, 160.);
   hist_mass_CP1 = new TH1F("hist_mass_CP1","hist_mass_CP1 ;m_{#gamma#gamma}; Events", 30, 105, 160.);
   hist_mass_CP4 = new TH1F("hist_mass_CP4","hist_mass_CP4 ;m_{#gamma#gamma}; Events", 30, 105, 160.);

   hist_pt1 = new TH1F("hist_pt1", "pt1; p_{t}^{#gamma#gamma}; Events", 30, 0, 200);
   hist_pt2 = new TH1F("hist_pt2", "pt2; p_{t}^{#gamma#gamma}; Events", 30, 0, 200);

   hist_eta1 = new TH1F("hist_eta1", "eta1; #eta_{#gamma#gamma}; Events", 30, -3, 3);
   hist_eta2 = new TH1F("hist_eta2", "eta2; #eta_{#gamma#gamma}; Events", 30, -3, 3);

   hist_energy1 = new TH1F("hist_energy1", "energy; #E_{#gamma#gamma}; Events", 30, 0, 500);
   hist_energy2 = new TH1F("hist_energy2", "energy; #E_{#gamma#gamma}; Events", 30, 0, 500);

   hist_dPhi = new TH1F("hist_dPhi", "; #Delta #phi_{#gamma#gamma}; Events", 30, -6, 6);

   hist_kincut0 = new TH1F("hist_kincut0", "; E/m_{#gamma#gamma}; Events", 30, 0, 5);
   hist_kincut1 = new TH1F("hist_kincut1", "; E/m_{#gamma#gamma}; Events", 30, 0, 5);

   c = new TCanvas("c", "c", 1200, 600);
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
   //TODO: Add histograms for photon identities, pt, energy etc..
   //       Se at ting ser fornuftig ut.

   fReader.SetLocalEntry(entry);
   TString option = GetOption();

   //Count total number of events.
   nEvents_tot++;

   // Set scale factors
   Float_t scaleFactor = 1.0;
   Float_t sf = ((*XSection)*10.6*1000)/(*SumWeights);   //pb fb osv
   if(p_option == "mc"){
      scaleFactor = sf*(*mcWeight)*(*scaleFactor_PILEUP)*(*scaleFactor_PHOTON)*(*scaleFactor_PhotonTRIGGER);
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
       //dPhi = dPhi < TMath::Pi() ? dPhi : 2*TMath::Pi() - dPhi;
       float mass = sqrt(2*photon1.Pt()*photon2.Pt()*(cosh(dEta) - cos(dPhi)));

       // Cut on known mass window
       if(!(mass > 105. && mass < 160.)){return kTRUE;}
       nEvents4++;

       // Kinematic selection requires ET/m > 0.35 for leading and 0.25 for subleading
       hist_kincut0->Fill(photon1.E()/mass, scaleFactor);
       if (!(photon1.E()/mass > 0.35 && photon2.E()/mass > 0.25)){return kTRUE;}
       nEvents5++;
       hist_kincut1->Fill(photon1.E()/mass, scaleFactor);

       hist_pt1->Fill(photon1.Pt(), scaleFactor);
       hist_pt2->Fill(photon2.Pt(), scaleFactor);

       hist_eta1->Fill(photon1.Eta(), scaleFactor);
       hist_eta2->Fill(photon2.Eta(), scaleFactor);

       hist_energy1->Fill(photon1.E(), scaleFactor);
       hist_energy2->Fill(photon2.E(), scaleFactor);

       hist_dPhi->Fill(dPhi, scaleFactor);

       hist_mass_CP1->Fill(mass, scaleFactor);

       if(abs(photon1.Eta()) <= 0.75 && abs(photon2.Eta())<=0.75){
          /*Central region - best mass resolution*/
          nEvents6++;
          hist_mass_CP2->Fill(mass, scaleFactor);
          if (photon_convType[0] == 0 && photon_convType[1] == 0) {
             /* only the unconverted ones*/
             hist_mass_CP3->Fill(mass, scaleFactor);
             return kTRUE;
          }
          hist_mass_CP4->Fill(mass, scaleFactor);
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
   write_histogram(p_option, option);
   write_div(option);
   write_info(p_option, option);
}


void analysis::write_histogram(string folder, TString option){
   TString indir = "output/"+folder+"/";
   TString filename = "outfile."+option+".root";
   TFile file(indir+filename, "RECREATE");
   hist_mass_CP1->Write();
   hist_mass_CP3->Write();
   hist_mass_CP2->Write();
   hist_mass_CP4->Write();
   file.Close();
   cout << "histograms saved in:  " << indir+filename << endl;
   hist_mass_CP1->Reset();
   hist_mass_CP3->Reset();
   hist_mass_CP2->Reset();
   hist_mass_CP4->Reset();
}

void analysis::write_info(string folder, TString option){
   ofstream info;
   TString indir = "output/"+folder+"/";
   TString filename2 = "info_"+option+".txt";
   info.open(indir+filename2);
   info << "total_events"        << "  " << nEvents_tot << "  " <<  "1" << endl;
   info << "Diphoton_trigger"    << "  " << nEvents1    << "  " << nEvents1/nEvents_tot << endl;
   info << "Exactly_two_photons" << "  " << nEvents2    << "  " << nEvents2/nEvents_tot << endl;
   info << "Preselection_cuts"   << "  " << nEvents3    << "  " << nEvents3/nEvents_tot << endl;
   info << "Mass_window_cut"     << "  " << nEvents4    << "  " << nEvents4/nEvents_tot << endl;
   info << "Kinematic_selection" << "  " << nEvents5    << "  " << nEvents5/nEvents_tot << endl;
   info << "Central_region"      << "  " << nEvents6    << "  " << nEvents6/nEvents_tot << endl;
   info.close();
   cout << "info saved in:        " << filename2 << endl;
}

void analysis::write_div(TString option){
   TString indir = "output/";
   TString filename = "div."+option+".root";
   TFile file(indir+filename, "RECREATE");
   hist_pt1->Write();
   hist_pt2->Write();
   hist_eta1->Write();
   hist_eta2->Write();
   hist_energy1->Write();
   hist_energy2->Write();
   hist_dPhi->Write();
   hist_kincut0->Write();
   hist_kincut1->Write();
   file.Close();
   cout << "histograms2 saved in: " << indir+filename << endl;
   hist_pt1->Reset();
   hist_pt2->Reset();
   hist_eta1->Reset();
   hist_eta2->Reset();
   hist_energy1->Reset();
   hist_energy2->Reset();
   hist_dPhi->Reset();
   hist_kincut0->Reset();
   hist_kincut1->Reset();
}
