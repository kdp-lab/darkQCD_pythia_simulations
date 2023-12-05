import uproot
import numpy as np
import glob
import multiprocessing
import os
import h5py

def count_particles_satisfying_cuts(file_path, tree_name, cuts):

    with uproot.open(file_path) as file:

        # Access the tree inside the ROOT file
        tree = file[tree_name]

        # Get all data for particles at once
        branches = ["pt", "eta", "status", "xDec", "yDec", "id"]
        x = {b : tree[b].array() for b in branches}

        # compute variables
        x["Lxy"] = np.sqrt(x["xDec"]**2 + x["yDec"]**2)

    # Apply cuts to count particles satisfying the conditions
    cut = (np.abs(x["id"])==cuts["id"]) * (x["pt"] > cuts["pt_min"]) * (abs(x["eta"]) < cuts["eta_max"]) * (x["Lxy"] < cuts["Lxy_max"])

    # count number of particles per event
    counts = np.sum(cut,axis=1)
    return [np.mean(counts), np.std(counts), counts]

def process_file(file_path, tree_name, cuts, results_dict):
    results_dict[file_path] = count_particles_satisfying_cuts(file_path, tree_name, cuts)

if __name__ == "__main__":

    # Replace with your ROOT file path and tree name
    file_paths = sorted(glob.glob("outdir/etaMassScanCtauMin/higgs_portal_m=*_xio=*_xil=*_ctauMin.root"))
    tree_name = "t"

    # Define your cuts
    cuts = {
        "id" : 4900111,
        "pt_min": 5, # GeV
        "eta_max": 2.4, 
        "Lxy_max": 1000, # mm
    }

    # Use a Manager to share the dictionary among processes
    manager = multiprocessing.Manager()
    results = manager.dict()

    # Number of CPU cores for parallel processing
    num_cores = multiprocessing.cpu_count()
    num_cores = 10 if num_cores > 10 else num_cores

    # Create a pool of processes
    pool = multiprocessing.Pool(processes=num_cores)

    # Launch tasks for each file in parallel
    for file_path in file_paths:
        print(file_path)
        # process_file(file_path, tree_name, cuts, results)
        pool.apply_async(process_file, (file_path, tree_name, cuts, results))

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    print(results)

    # Access results from the dictionary once all files are processed
    # for file_path, count_per_event in results.items():
    #     print(file_path, count_per_event)

    xio = 1
    xil = 1
    m_eta = list(range(1,31))
    mean = [results[f"outdir/etaMassScanCtauMin/higgs_portal_m={m}_xio={xio}_xil={xil}_ctauMin.root"][0] for m in m_eta]
    std = [results[f"outdir/etaMassScanCtauMin/higgs_portal_m={m}_xio={xio}_xil={xil}_ctauMin.root"][1] for m in m_eta]
    counts = [results[f"outdir/etaMassScanCtauMin/higgs_portal_m={m}_xio={xio}_xil={xil}_ctauMin.root"][2] for m in m_eta]

    # save to file
    outFileName = "outdir/etaMassScanCtauMin/resultsNew.h5"
    # Open the HDF5 file in write mode
    with h5py.File(outFileName, "w") as f:
        # Create datasets within the HDF5 file and write the arrays
        f.create_dataset("m_eta", data=m_eta)
        f.create_dataset("mean", data=mean)
        f.create_dataset("std", data=std)
        f.create_dataset("counts", data=counts)

