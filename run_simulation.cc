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

//==========================================================================

int main() {

  // Generator.
  Pythia pythia;

  // Shorthand for the event record in pythia.
  Event& event = pythia.event;

  // Read in commands from external file.
  pythia.readFile("higgs_portal.cmnd");

  // Extract settings to be used in the main program.
  int nEvent = pythia.mode("Main:numberOfEvents");
  int nAbort = pythia.mode("Main:timesAllowErrors");

  // Initialize.
  pythia.init();



  // Create root file
  TFile* rootFile = new TFile("higgs_portal.root","RECREATE");

  // Create a TTree
  TTree* myTree = new TTree("higgsTree","Example TTree");



  int iEvent;
  int entries;
  int id;
  double m;

  myTree->Branch("EventNumber",&iEvent,"EventNumber/I");
  myTree->Branch("NumberEntries",&entries,"NumberEntries/I");
  myTree->Branch("Id",&id,"Id/I");
  myTree->Branch("Mass",&m,"Mass/D");


  // Begin event loop.
  int iAbort = 0;
  for (iEvent = 0; iEvent < nEvent; ++iEvent) {

    if(!pythia.next()) continue;


    entries = event.size();

    std::cout << "Event: " << iEvent << std::endl;
    std::cout << "Event size: " << entries << std::endl;

    for(int j=0;j<entries;j++){
      id = pythia.event[j].id();
      m = pythia.event[j].m();
      //std::cout << "Id: "<< id << "     mass: "<< m << std::endl;

      myTree->Fill();
   }


  } 

  myTree->Write();  



  rootFile->Close();

  return 0;
}
