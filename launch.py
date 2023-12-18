import subprocess
import multiprocessing

def run_executable(executable_path, options):
    command = [executable_path] + options
    subprocess.run(command)

if __name__ == "__main__":

    # List of options for each execution
    path_to_executable = "./bin/higgsPortal.exe"
    xio = 1
    xil = 1
    options_list = []
    for m in range(1,31):
        card = f"cards/etaMassScanCtauMin/higgs_portal_m={m}_xio={xio}_xil={xil}_ctauMin.cmnd"
        outFileName = f"outdir/pythia8235/etaMassScanCtauMin/higgs_portal_m={m}_xio={xio}_xil={xil}_ctauMin.root"
        nevents = str(10000)
        options_list.append([card, outFileName, nevents])

    # List of CPU cores to use for parallel execution
    num_cores = multiprocessing.cpu_count()
    # num_cores = 10 if num_cores > 10 else num_cores

    # Create a pool of processes to run in parallel
    pool = multiprocessing.Pool(num_cores)
    
    # Launch the executable N times in parallel with different options
    pool.starmap(run_executable, [(path_to_executable, options) for options in options_list])

    # Close the pool of processes
    pool.close()
    pool.join()
