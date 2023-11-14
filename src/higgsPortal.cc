/*

  Authors: 
  Matias Mantinan
  Anthony Badea
  Karri DiPetrillo

  Description:
  Script to generate pythia samples

*/

// c, pythia, root includes
#include <iostream>
#include "Pythia8/Pythia.h"
#include "TFile.h"
#include "TTree.h"

// declare pythia8 namespace
using namespace Pythia8;

// print a message to the console
void msg(string m){
  printf("\r%s",m.c_str());                               
  std::cout << std::endl;
}

// progress bar for the people taken from alex tuna and ann wang
void pbftp(double time_diff, int nprocessed, int ntotal){
  if(nprocessed%10 == 0){
    double rate      = (double)(nprocessed+1)/time_diff;
    std::cout << "\r > " << nprocessed << " / " << ntotal
	      << " | "   << std::fixed << std::setprecision(1) << 100*(double)(nprocessed)/(double)(ntotal) << "%"
	      << " | "   << std::fixed << std::setprecision(1) << rate << "Hz"
	      << " | "   << std::fixed << std::setprecision(1) << time_diff/60 << "m elapsed"
	      << " | "   << std::fixed << std::setprecision(1) << (double)(ntotal-nprocessed)/(rate*60) << "m remaining"
	      << std::flush;
  }
  // add new line at end of events
  if (nprocessed+1 == ntotal){
    msg("");
  }
}

int main() {

  // Generator.
  Pythia pythia;

  // Shorthand for the event record in pythia.
  Event& event = pythia.event;

  // Read in commands from external file.
  pythia.readFile("./cards/higgs_portal.cmnd");

  // Extract settings to be used in the main program.
  int nEvents = pythia.mode("Main:numberOfEvents");
  int nAborts = pythia.mode("Main:timesAllowErrors");

  // Initialize.
  pythia.init();

  // Create root file and tree
  TFile* f = new TFile("myTree.root","RECREATE");
  TTree* t = new TTree("t","t");

  // initialize branches variables
  int nParticles;
  std::vector<int> *id = 0;
  std::vector<int> *status = 0;
  std::vector<double> *mass = 0;
  std::vector<double> *pt = 0;
  std::vector<double> *eta = 0;
  std::vector<double> *phi = 0;

  // initialize branches
  t->Branch("nParticles", &nParticles);
  t->Branch("id", &id);
  t->Branch("status", &status);
  t->Branch("mass", &mass);
  t->Branch("pt", &pt);
  t->Branch("eta", &eta);
  t->Branch("phi", &phi);

  // time keeper for progress bar
  std::chrono::time_point<std::chrono::system_clock> time_start;
  std::chrono::duration<double> elapsed_seconds;
  time_start = std::chrono::system_clock::now();

  for (int iE = 0; iE < nEvents; ++iE) {

    if(!pythia.next()) continue;

    // progress bar
    elapsed_seconds = (std::chrono::system_clock::now() - time_start);
    pbftp(elapsed_seconds.count(), iE, nEvents);

    // clear for new event
    id->clear();
    status->clear();
    mass->clear();
    pt->clear();
    eta->clear();
    phi->clear();
    
    // get event level information
    nParticles = event.size();

    // loop over the particles. available properties listed here https://pythia.org/latest-manual/ParticleProperties.html
    for(int iP=0; iP<nParticles; iP++){
      id->push_back(pythia.event[iP].id());
      status->push_back(pythia.event[iP].status());
      mass->push_back(pythia.event[iP].m());
      pt->push_back(pythia.event[iP].pT());
      eta->push_back(pythia.event[iP].eta());
      phi->push_back(pythia.event[iP].phi());
   }

    // fill tree on each particle loop
    t->Fill();
  } 

  // write and cleanup
  t->Write();  
  f->Close();

  return 0;
}
