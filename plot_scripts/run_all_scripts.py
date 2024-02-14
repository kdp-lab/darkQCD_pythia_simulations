import subprocess


for m in range(1,31):
    """

    command  = f"python3 energy_histogram/plot_energy_hist_all_status1.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    command  = f"python3 energy_histogram/plot_energy_hist_all.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 energy_histogram/plot_energy_hist_dark.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    """
    command  = f"python3 event_level/event_level_hists.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    

    command  = f"python3 eta_histogram/plot_eta_hist_all_status1.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    command  = f"python3 eta_histogram/plot_eta_hist_all.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 eta_histogram/plot_eta_hist_dark.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 mass_histogram/plot_mass_hist_all_status1.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    command  = f"python3 mass_histogram/plot_mass_hist_all.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 mass_histogram/plot_mass_hist_dark.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 phi_histogram/plot_phi_hist_all_status1.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    command  = f"python3 phi_histogram/plot_phi_hist_all.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 phi_histogram/plot_phi_hist_dark.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 pt_histogram/plot_pt_hist_all_status1.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)

    command  = f"python3 pt_histogram/plot_pt_hist_all.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)


    command  = f"python3 pt_histogram/plot_pt_hist_dark.py -i ../output/higgs_portal_m\={m}_xio\=1_xil\=1_ctauMin.hepmc"
    subprocess.call(command,shell=True)
