// main03.cc is a part of the PYTHIA event generator.
// Copyright (C) 2023 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Keywords: basic usage; process selection; command file; python; matplotlib

// This is a simple test program.
// It illustrates how different processes can be selected and studied.
// All input is specified in the main03.cmnd file.
// Also illustrated output to be plotted by Python/Matplotlib/pyplot.
#include <iostream>
#include "Pythia8/Pythia.h"
#include "TFile.h"
#include "TTree.h"

using namespace Pythia8;

void msg(string m){
  printf("\r%s",m.c_str());                               
  std::cout << std::endl;
}

void pbftp(double time_diff, int nprocessed, int ntotal){
  /* progress bar for the people taken from alex tuna and ann wang */
  if(nprocessed%10 == 0){
    double rate      = (double)(nprocessed+1)/time_diff;
    std::cout << "\r > " << nprocessed << " / " << ntotal
	      << " | "   << std::fixed << std::setprecision(1) << 100*(double)(nprocessed)/(double)(ntotal) << "%"
	      << " | "   << std::fixed << std::setprecision(1) << rate << "Hz"
	      << " | "   << std::fixed << std::setprecision(1) << time_diff/60 << "m elapsed"
	      << " | "   << std::fixed << std::setprecision(1) << (double)(ntotal-nprocessed)/(rate*60) << "m remaining"
	      << std::flush;

    // add new line at end of events
    if (nprocessed+1 == ntotal){
      msg("");
    }
  }
}

int main() {

  // Generator.
  Pythia pythia;

  // Shorthand for the event record in pythia.
  Event& event = pythia.event;

  // Read in commands from external file.
  pythia.readFile("higgs_portal.cmnd");

  // Extract settings to be used in the main program.
  int nEvents = pythia.mode("Main:numberOfEvents");
  int nAborts = pythia.mode("Main:timesAllowErrors");

  // Initialize.
  pythia.init();

  // Create root file
  TFile* f = new TFile("myTree.root","RECREATE");
  // Create a TTree
  TTree* t = new TTree("t","t");

  int nParticles;
  std::vector<int> *id = 0;
  std::vector<double> *mass = 0;
  std::vector<double> *pt = 0;
  std::vector<double> *eta = 0;
  std::vector<double> *phi = 0;

  t->Branch("nParticles", &nParticles);
  t->Branch("id", &id);
  t->Branch("mass", &mass);
  t->Branch("pt", &pt);
  t->Branch("eta", &eta);
  t->Branch("phi", &phi);
  
  // generate events
  std::cout<<"Generating events"<<std::endl;

  // time keeper
  std::chrono::time_point<std::chrono::system_clock> time_start;
  std::chrono::duration<double> elapsed_seconds;
  time_start = std::chrono::system_clock::now();

  for (int iE = 0; iE < nEvents; ++iE) {

    if(!pythia.next()) continue;

    // progress bar
    elapsed_seconds = (std::chrono::system_clock::now() - time_start);
    pbftp(elapsed_seconds.count(), iE, nEvents);

    // get event level information
    nParticles = event.size();

    // loop over the particles
    for(int iP=0; iP<nParticles; iP++){
      id->push_back(pythia.event[iP].id());
      mass->push_back(pythia.event[iP].m());
      pt->push_back(pythia.event[iP].pT());
      eta->push_back(pythia.event[iP].eta());
      phi->push_back(pythia.event[iP].phi());
   }

    t->Fill();
  } 

  // write and cleanup
  t->Write();  
  f->Close();

  return 0;
}
