# darkQCD_pythia_simulations

# setup environment
setupATLAS
lsetup "python 3.9.18-x86_64-centos7"
lsetup "root 6.28.08-x86_64-centos7-gcc11-opt"

# first get pythia 8.307
'''
wget https://pythia.org/download/pythia83/pythia8307.tgz
tar -xvf pythia8307.tgz
cd pythia8307
make
'''

# update this path to your pythia path in Makefile.inc
PREFIX=/home/abadea/pythia8307

# setup this repo and run test
cd darkQCD_pythia_simulations
make all
./bin/higgsPortal.exe cards/higgs_portal.cmnd myTree.root 100