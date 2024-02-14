import pyhepmc
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
import pandas as pd
from particle import Particle
from particle import PDGID

pid_translator = {
        11:"electron",
        -11:"positron",
        12:"electron neutrino",
        -12:"electron antineutrino",
        13:"muon",
        -13:"antimuon",
        14:"muon neutrino",
        -14:"muon antineutrino",
        15:"tau",
        -15:"antitau",
        16:"tau neutrino",
        -16:"tau antineutrino",
        130:"K0 L meson",
        321:"K+ meson",
        -321:"antiK+ meson",
        4900113:"spin 1 dark meson",
        4900111:"spin 0 dark messon",
        211:"pi+",
        -211:"pi-",
        22:"gamma",
        2112:"neutron",
        -2112:"antineutron",
        2212:"proton",
        -2212:"antiproton",
        }


pid_dark = {
        4900101:{"name":"qD","charge":1./3,"is_meson":False},
        -4900101:{"name":"antiqD","charge":-1./3,"is_meson":False},
        4900021:{"name":"gD","charge":0.,"is_meson":False},
        4900113:{"name":"omegaD","charge":1.,"is_meson":True},
        -490113:{"name":"antiomegaD","charge":-1.,"is_meson":True},
        4900111:{"name":"etaD","charge":0.,"is_meson":True},
        -4900111:{"name":"antietaD","charge":0.,"is_meson":True}
        }




if __name__ == "__main__":
    
    # user options
    parser = argparse.ArgumentParser(usage=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--inFileName", help="Input file name", default="test.hepmc")
    parser.add_argument("-o", "--outFileName", help="Output file name", default="out.txt")
    ops = parser.parse_args()

    # list for tracks
    #tracks = [] # cotb cota p flp localx localy pT
    fname = ops.inFileName
    outFile = (fname.split('/')[-1]).split('.')[0]

    # pyhepmc.open can read most HepMC formats using auto-detection
    with pyhepmc.open(fname) as f:
        # loop over events
        particle_id = []
        name = []
        charge = []
        event_number = []
        status = []
        mass = []
        pt = []
        eta = []
        phi = []
        energy = []
        is_meson = []

        numEvents = 0


        for iF, event in enumerate(f):
            # loop over particles
            numEvents += 1


            if iF >99:
                break # I just want to plot a few events
            
            print(f"Event {iF} has {len(event.particles)} particles")
            for particle in event.particles:
                

                # # to get the production vertex and position
                prod_vertex = particle.production_vertex
                prod_vector = prod_vertex.position
                prod_R = prod_vector.perp() # [mm]

                # # to get the decay vertex
                # decay_vertex = particle.end_vertex
                # decay_vector = decay_vertex.position
                
                # decide which particles to keep
                
                accept = (abs(particle.momentum.eta()) != float("inf")) # non infinite eta
                
                # for now I won't cut in final state partiles or particles in the detectors, I want to see intermediate particles too
                #accept *= (particle.status == 1) # final state particle
                #accept *= (particle.momentum.pt()>1)
                #accept *= ( (prod_R >= 30) * (prod_R <= 130) ) # within pixel detector ~ 30-130mm

                if not accept:
                    continue

                #print(particle.id, particle.pid, particle.status, particle.momentum.pt(), particle.momentum.eta(), particle.momentum.phi(), prod_vector.x, prod_vector.y)

                # track properties
                #eta = particle.momentum.eta()
                #phi = particle.momentum.phi()
                #p = particle.momentum.p3mod()
                #localx = prod_vector.x # this needs to be particle position at start of pixel detector or only save particles that are produced within epsilon distance of detector
                #localy = prod_vector.y # [mm]
                #pT = particle.momentum.pt()
                


                try: 
                    id = particle.pid
                    
                    if id in pid_dark:
                        n = pid_dark[id]["name"]
                        c = pid_dark[id]["charge"]
                        meson = pid_dark[id]["is_meson"]
                    else:
                        c = PDGID(particle.pid).charge
                        meson = PDGID(particle.pid).is_meson
                        n = Particle.from_pdgid(particle.pid).name

                except:
                    print("There was an error")

                particle_id.append(id)
                event_number.append(iF)
                status.append(particle.status)
                eta.append(particle.momentum.eta())
                phi.append(particle.momentum.phi())
                pt.append(particle.momentum.pt())
                mass.append(particle.momentum.m())
                energy.append(particle.momentum.e)

                name.append(n)
                charge.append(c)
                is_meson.append(meson)
                
        dict ={"id":particle_id,"name":name,"charge":charge,"event":event_number,"status":status,"mass":mass,"energy":energy,"pt":pt,"eta":eta,"phi":phi,"is_meson":is_meson}

        particles = pd.DataFrame(dict)


        #print(particles.head(100))


        dark_particles = []
        dark_quarks = []
        dark_mesons = []
        status1 = []
        sm_status1 = []
        reconstruct = []
        #sm_statis1_positive = []
        #sm_status1_negative = []


        for n in range(numEvents):
            status1.append(particles[(particles["event"]==n) & (particles["status"]==1)].shape[0])
            dark_particles.append(particles[(particles["event"]==n) & (particles["id"].isin(pid_dark))].shape[0])
            dark_mesons.append(particles[(particles["event"]==n) & (particles["id"].isin(pid_dark)) & (particles["is_meson"]==True)].shape[0])
            reconstruct.append(particles[(particles["event"]==n) & (particles["eta"].abs() < 2.5) & (particles["pt"]>1) & (particles["charge"]!=0)].shape[0])



        """
        outFolder = f"/local/d1/mmantinan/darkQCD_pythia_simulations/figures/event_level/{outFolder}"
        
        if not os.path.exists(outFolder):
            print(f"Creating directory {outFolder}")
            os.makedirs(outFolder)
        """
        
        outFolder = f"/local/d1/mmantinan/darkQCD_pythia_simulations/figures/event_level/status1"
        
        if not os.path.exists(outFolder):
            print(f"Creating directory {outFolder}")
            os.makedirs(outFolder)




        plt.style.use('ggplot')
        fig, ax = plt.subplots()
           

        #ax.scatter(etas,phis,label=f"Event {iF}: {len(event.particles)} particles", marker='.')
        #ax.hist(particles['mass'],range=(0,20),log=True,bins=50)
        ax.hist(status1,density=True,bins=20,label="status1 particles")
        ax.set_xlabel("number of particles")
        ax.set_ylabel("number of events")
        ax.set_title(f"status1 particles histogram")
            

        ax.legend()          


        #print(f"Saving figure: {outFolder}/status1_histogram.png")
        #plt.savefig(f"{outFolder}/status1_histogram.png")
        print(f"Saving figure: {outFolder}/{outFile}.png")
        plt.savefig(f"{outFolder}/{outFile}.png")

        plt.cla()



        outFolder = f"/local/d1/mmantinan/darkQCD_pythia_simulations/figures/event_level/dark"
        
        if not os.path.exists(outFolder):
            print(f"Creating directory {outFolder}")
            os.makedirs(outFolder)




        ax.hist(dark_particles,density=True,bins=20,label="dark particles")
        ax.set_xlabel("number of particles")
        ax.set_ylabel("number of events")
        ax.set_title(f"dark particles particles histogram")

        ax.legend()
            

        #print(f"Saving figure: {outFolder}/dark_histogram.png")
        #plt.savefig(f"{outFolder}/dark_histogram.png")
        print(f"Saving figure: {outFolder}/{outFile}.png")
        plt.savefig(f"{outFolder}/{outFile}.png")

        plt.cla()




        outFolder = f"/local/d1/mmantinan/darkQCD_pythia_simulations/figures/event_level/dark_mesons"
        
        if not os.path.exists(outFolder):
            print(f"Creating directory {outFolder}")
            os.makedirs(outFolder)


        ax.hist(dark_mesons,density=True,bins=20,label="dark mesons")
        ax.set_xlabel("number of particles")
        ax.set_ylabel("number of events")
        ax.set_title(f"dark mesons histogram")

        ax.legend()
            

        #print(f"Saving figure: {outFolder}/dark_mesons_histogram.png")
        #plt.savefig(f"{outFolder}/dark_mesons_histogram.png")
        print(f"Saving figure: {outFolder}/{outFile}.png")
        plt.savefig(f"{outFolder}/{outFile}.png")


        plt.cla()


        outFolder = f"/local/d1/mmantinan/darkQCD_pythia_simulations/figures/event_level/reconstruct"
        
        if not os.path.exists(outFolder):
            print(f"Creating directory {outFolder}")
            os.makedirs(outFolder)



        ax.hist(reconstruct,density=True,bins=20,label="reconstruct particles")
        ax.set_xlabel("number of particles")
        ax.set_ylabel("number of events")
        ax.set_title(f"particles pt>1GeV & status=1 & |eta|<2.5 & charged")

        ax.legend()
            

        #print(f"Saving figure: {outFolder}/reconstruct_histogram.png")
        #plt.savefig(f"{outFolder}/reconstruct_histogram.png")
        print(f"Saving figure: {outFolder}/{outFile}.png")
        plt.savefig(f"{outFolder}/{outFile}.png")


        plt.cla()
