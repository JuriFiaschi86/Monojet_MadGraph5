#! /usr/bin/python3

import os
import shutil
import re
import sys
import glob
import subprocess
import datetime
import pandas
import argparse
import math

from write_MG5_shell import write_mg5_shell
from write_param_card import write_param_card
from write_run_card import write_run_card
from write_madevent_shell import write_madevent_shell
from analyse_lhco import read_lhco
from analyse_lhco import events_analysis
from write_scan_summary import scan_summary
from plot_results import plot_results

class params_couplings():
    ### Couplings to scalar mediator
    gSXr = 0
    gSXc = 0
    gSXd = 0
    gSd11 = 0
    gSu11 = 0
    gSd22 = 0
    gSu22 = 0
    gSd33 = 0
    gSu33 = 0
    gSg = 0
    ### Couplings to pseudoscalar mediator
    gPXd = 0
    gPd11 = 0
    gPu11 = 0
    gPd22 = 0
    gPu22 = 0
    gPd33 = 0
    gPu33 = 0
    gPg = 0
    ### Couplings to vector mediator
    gVXc = 0
    gVXd = 1
    gVd11 = 0.25
    gVu11 = 0.25
    gVd22 = 0.25
    gVu22 = 0.25
    gVd33 = 0.25
    gVu33 = 0.25
    ### Couplings to axial mediator
    gAXd = 0
    gAd11 = 0
    gAu11 = 0
    gAd22 = 0
    gAu22 = 0
    gAd33 = 0
    gAu33 = 0
    
class params_masses():
    ### real scalar singlet DM
    MXr = 0
    ### complex scalar singlet DM
    MXc = 0
    ### fermion doublet DM
    MXd = 10
    ### scalar mediator
    MY0 = 1000000
    ### vector mediator
    MY1 = 1000
    ### scalar mediator width
    WY0 = 10
    ### vector mediator width (not sure if this gets calculated or shall be putted by hand)
    WY1 = "Auto"

class params_run():
    ### number of events
    nevents = 100
    ### LHAPDF PDF set id
    lhapdfid = 262000
    #lhapdfid = 247000
    ### ren/fact scale choice
    scale_choice = 0

### Initialize classes
results = []
efficiencies = []

couplings = params_couplings()
masses = params_masses()
run = params_run()

########################
### SETTING THE LOOP ###
########################


### Set the parameters of the runs
run.nevents = 10000
run.lhapdfid = 262000 ### NNPDF3.0_LO
run.scale_choice = 0 ### customised scale choice

### Set the couplings
#### First test run will be on axial mediator
#couplings.gVXd = 0
#couplings.gVd11 = 0
#couplings.gVu11 = 0
#couplings.gVd22 = 0
#couplings.gVu22 = 0
#couplings.gVd33 = 0
#couplings.gVu33 = 0

#couplings.gAXd = 1
#couplings.gAd11 = 0.25
#couplings.gAu11 = 0.25
#couplings.gAd22 = 0.25
#couplings.gAu22 = 0.25
#couplings.gAd33 = 0.25
#couplings.gAu33 = 0.25

### Right mediator with Axial coupling to DM
guoriginal = 0.25
gdoriginal = 0.25
f = pow(guoriginal, 2) + pow(gdoriginal, 2)
r = 1.

gu = math.sqrt(f) / math.sqrt(1 + pow(r, 2))
gd = r * gu

couplings.gVXd = 1
couplings.gVd11 = gd / math.sqrt(2)
couplings.gVu11 = gu / math.sqrt(2)
couplings.gVd22 = gd / math.sqrt(2)
couplings.gVu22 = gu / math.sqrt(2)
couplings.gVd33 = gd / math.sqrt(2)
couplings.gVu33 = gu / math.sqrt(2)

couplings.gAXd = 0
couplings.gAd11 = -couplings.gVd11
couplings.gAu11 = -couplings.gVu11
couplings.gAd22 = -couplings.gVd22
couplings.gAu22 = -couplings.gVu22
couplings.gAd33 = -couplings.gVd33
couplings.gAu33 = -couplings.gVu33

### Set the masses
masses.MY0 = 100000 ### decouple scalar mediator (it should not be needed)
masses.WY0 = 10 ### dummy value for the scalar mediator width

masses.WY1 = "Auto" ### vector mediator automatic width

### Scan range

mZpr_min = 200
mZpr_max = 2700
mZpr_bin = 100

mDM_min = 50
mDM_max = 1000
mDM_bin = 50

#######################
### SET DIRECTORIES ###
#######################

current_dir = os.getcwd() + "/"

#### Get MG5_aNLO path
#command = "locate -b 'MG5_aMC_v'"
#call = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
#(call_output, call_error) = call.communicate()
#call_status = call.wait()
#path_Madgraph = call_output.decode("utf-8").split()[0] + "/"

path_Madgraph = "/srv/pheno_dir/tools/MG5_aMC_v2_8_2/"

model = "DMsimp_UFO"


###################
### SET PROCESS ###
###################

mediator_type = 0

### Not yet completely implemented
if ((couplings.gVd11) and (couplings.gAd11) and (couplings.gVu11) and (couplings.gAu11) and (couplings.gAXd) and (couplings.gVXd)):
    mediator_type = 1
    mediator_type_string = "vector_axial"
    process_name = mediator_type_string + "_monojet_gVq_" + str(couplings.gVd11) + "_gVxi_" + str(couplings.gVXd) + "_gAq_" + str(couplings.gAd11) + "_gAxi_" + str(couplings.gAXd)
    
elif ((couplings.gVd11 == couplings.gAd11) and (couplings.gVu11 == couplings.gAu11) and (couplings.gVXd) and not(couplings.gAXd)):
    mediator_type = 4
    mediator_type_string = "left_vector"
    process_name = mediator_type_string + "_monojet_gdL_" + str(float(format(couplings.gVd11, ".3f"))) + "_guL_" + str(float(format(couplings.gVu11, ".3f"))) + "_gVxi_" + str(couplings.gVXd)
elif ((couplings.gVd11 == couplings.gAd11) and (couplings.gVu11 == couplings.gAu11) and not(couplings.gVXd) and (couplings.gAXd)):
    mediator_type = 5
    mediator_type_string = "left_axial"
    process_name = mediator_type_string + "_monojet_gdL_" + str(float(format(couplings.gVd11, ".3f"))) + "_guL_" + str(float(format(couplings.gVu11, ".3f"))) + "_gAxi_" + str(couplings.gAXd)
elif ((couplings.gVd11 == -couplings.gAd11) and (couplings.gVu11 == -couplings.gAu11) and (couplings.gVXd) and not(couplings.gAXd)):
    mediator_type = 6
    mediator_type_string = "right_vector"
    process_name = mediator_type_string + "_monojet_gdR_" + str(float(format(couplings.gVd11, ".3f"))) + "_guR_" + str(float(format(couplings.gVu11, ".3f"))) + "_gVxi_" + str(couplings.gVXd)
elif ((couplings.gVd11 == -couplings.gAd11) and (couplings.gVu11 == -couplings.gAu11) and not(couplings.gVXd) and (couplings.gAXd)):
    mediator_type = 7
    mediator_type_string = "right_axial"
    process_name = mediator_type_string + "_monojet_gdR_" + str(float(format(couplings.gVd11, ".3f"))) + "_guR_" + str(float(format(couplings.gVu11, ".3f"))) + "_gAxi_" + str(couplings.gAXd)

elif ((couplings.gVd11) and (couplings.gVu11) and (couplings.gVXd)):
    mediator_type = 2
    mediator_type_string = "vector"
    if (couplings.gVd11 == couplings.gVu11):
        process_name = mediator_type_string + "_monojet_gq_" + str(couplings.gVd11) + "_gxi_" + str(couplings.gVXd)
    else:
        process_name = mediator_type_string + "_monojet_gd_" + str(couplings.gVd11) + "_gu_" + str(couplings.gVu11) + "_gxi_" + str(couplings.gVXd)

elif ((couplings.gAd11) and (couplings.gAu11) and (couplings.gAXd)):
    mediator_type = 3
    mediator_type_string = "axial"
    if (couplings.gAd11 == couplings.gAu11):
        process_name = mediator_type_string + "_monojet_gq_" + str(couplings.gAd11) + "_gxi_" + str(couplings.gAXd)
    else:
        process_name = mediator_type_string + "_monojet_gd_" + str(couplings.gAd11) + "_gu_" + str(couplings.gAu11) + "_gxi_" + str(couplings.gAXd)

if not(mediator_type):
    sys.exit("The Zpr couplings you have chosen are incorrect\n")
if (mediator_type == 1):
    sys.exit("Sorry the general case with mediator with all different couplings is not yet implemented\nStay tuned for updates :)\n")

process_path = path_Madgraph + process_name + "/"
output_folder_analysed_events = current_dir + process_name + "_Analysed_Events/"


#############
### FLAGS ###
#############

### Check if process folder has been already created
if os.path.exists(process_path):
    flag_generate_process = False
else: 
    flag_generate_process = True

### Flag to generate the events. If events have already been generated, can be switched off
#flag_generate_events = False
flag_generate_events = True

### Flag to run the analysis
flag_run_analysis = False

parser = argparse.ArgumentParser(description="Monojet analysis script. Select the option 'analysis' to run the analysis (i.e. ./main.py analysis), or the option 'plot' to produce the plot (i.e. ./main.py plot)")
parser.add_argument("option")
args = parser.parse_args()
if (args.option == "analysis"):
    flag_run_analysis = True
elif (args.option == "plot"):
    flag_run_analysis = False
else:
    sys.exit("Choose between the option 'analysis' to run the analysis (i.e. ./main.py analysis)\nand the option 'plot' to produce the plot (i.e. ./main.py plot)")

############################
### ASK FOR CONFIRMATION ###
############################

if flag_run_analysis:

    #print("########################################")
    #print("You are about to run the following scan:")
    #print("########################################")
    #print("Monojet analysis for " + mediator_type_string + " mediator with couplings:")
    #if (mediator_type == 2):
        #print("gd = " + str(couplings.gVd11) + " ; gu = " + str(couplings.gVu11) + " ; gxi = " + str(couplings.gVXd))
    #elif (mediator_type == 3):
        #print("gd = " + str(couplings.gAd11) + " ; gu = " + str(couplings.gAu11) + " ; gxi = " + str(couplings.gAXd))
    #elif (mediator_type == 4):
        #print("gdL = " + str(couplings.gVd11) + " ; guL = " + str(couplings.gVu11) + " ; gVxi = " + str(couplings.gVXd))
    #elif (mediator_type == 5):
        #print("gdL = " + str(couplings.gVd11) + " ; guL = " + str(couplings.gVu11) + " ; gAxi = " + str(couplings.gAXd))
    #elif (mediator_type == 6):
        #print("gdR = " + str(couplings.gVd11) + " ; guR = " + str(couplings.gVu11) + " ; gVxi = " + str(couplings.gVXd))
    #elif (mediator_type == 7):
        #print("gdR = " + str(couplings.gVd11) + " ; guR = " + str(couplings.gVu11) + " ; gAxi = " + str(couplings.gAXd))
    #print("Scan range:")
    #print("mZpr in [" + str(mZpr_min) + ", " + str(mZpr_max) + "] GeV with bins of " + str(mZpr_bin) + " GeV")
    #print("mDM in [" + str(mDM_min) + ", " + str(mDM_max) + "] GeV with bins of " + str(mDM_bin) + " GeV")
    #print("Number of events for each paramter space points = " + str(run.nevents))
    #print("NOTE: points with (mZpr < 2 * mDM) will be skipped.")
    #print("########################################")
    #if flag_generate_process:
        #print("It appears this is the first time you run this process, so the process folder will be generated.")
    #else:
        #print("It appears the process has already been generated. Your older results will not be deleted.")
    #print("\n")
    #if flag_generate_events:
        #print("Now new events will be generated. Events generated in the past will be kept in the respective folder, but will not be used in the analysis")
        #print("If instead you do not want to generate the events, switch the 'flag_generate_events' to False")
    #else:
        #print("You are not going to generate new events. If all the necessary events in the scan have already been generated, then they will be analysed, otherwise the code will stop when the events are not found.")
        #print("NOTE: make sure the number of events you are asking for (" + str(run.nevents) + ") correspond to the number of events that have already been generated.")
        #print("If instead you want to generate the events, switch the 'flag_generate_events' to True")
    #print("\n")
    #confirm = input("Do you want to continue? [y,n]\n").lower()
    #while confirm not in ["y", "n"]:
        #print("Please, type 'y' or 'n'")
        #confirm = input("Do you want to continue? [y,n]")
    #if (confirm == "n"):
        #sys.exit("As you prefer. Exiting now. Have a good day!\n")


    ########################
    ### GENERATE PROCESS ###
    ########################

    ### This would be done only once
    if flag_generate_process:

        ### Write MG5 shell script
        write_mg5_shell(model, process_name)

        ### Run MG5
        if os.path.exists(path_Madgraph + process_name):
            shutil.rmtree(path_Madgraph + process_name)

        os.chdir(path_Madgraph)
        command = "./bin/mg5_aMC " + current_dir + "mg5_shell.sh"
        os.system(command)
        os.chdir(current_dir)

        ### Copy setscale.f
        if os.path.exists(process_path + "SubProcesses/setscales.f"):
            os.remove(process_path + "SubProcesses/setscales.f")
        shutil.copy2(current_dir + "setscales.f", process_path + "SubProcesses/")


    ######################
    ### START THE LOOP ###
    ######################

    mZpr_list = list(range(mZpr_min, mZpr_max + mZpr_bin, mZpr_bin))
    mDM_list = list(range(mDM_min, mDM_max + mDM_bin, mDM_bin))

    for mZpr in mZpr_list:
        for mDM in mDM_list:
        
            #if (2*mDM > mZpr): continue ### skip points with off-shell Z' decay into DM
            if (((mDM > 0.5*mZpr + 100) or (mDM < 0.5*mZpr - 150)) and (mZpr < 2000)): continue ### skip points far from the on-shell limit
            if ((mZpr >= 2000) and (mDM > 0.5*mZpr)): continue ### for sufficiently heavy Zpr compute also small DM points, but do not go above on-shell limit
                
            masses.MY1 = mZpr
            masses.MXd = mDM
            
            print("\n")
            print("###########################################")
            print("Analysing mZpr = " + str(mZpr) + " & mDM = " + str(mDM))
            print("###########################################")
            
            parameter_space_point = "psp_mZpr_" + str(masses.MY1) + "_mDM_" + str(masses.MXd)
            
            output_folder_events_lhco = current_dir + process_name + "_Events/"
            lhco_filename = "events_" + parameter_space_point + ".lhco"
            lhco_file_path = output_folder_events_lhco + lhco_filename
            
            if not((flag_generate_events) or (os.path.exists(process_path + "Events/" + parameter_space_point)) or (os.path.exists(lhco_file_path))):
                sys.exit("The events for this parameter space point have not been generated.\nSwitch on 'flag_generate_events' to generate the events\n")
            
            if flag_generate_events:
                
                ########################
                ### WRITE PARAM CARD ###
                ########################
                
                write_param_card(process_path, couplings, masses)
                
                ######################
                ### RUN PARAM CARD ###
                ######################

                write_run_card(process_path, run)
                
                ####################
                ### RUN MADEVENT ###
                ####################

                if os.path.exists(current_dir + "madevent_shell.sh"):
                    os.remove(current_dir + "madevent_shell.sh")

                write_madevent_shell(parameter_space_point)

                ### Delete RunWeb if exists
                if os.path.exists(process_path + "RunWeb"):
                    os.remove(process_path + "RunWeb")

                ### Begin time count
                start = datetime.datetime.now()

                ### Generate events
                os.chdir(process_path)
                command = "./bin/madevent " + current_dir + "madevent_shell.sh"
                os.system(command)
                os.chdir(current_dir)

                ### End time count
                end = datetime.datetime.now()
                elapsed_time = end - start

                ### Delete RunWeb if exists
                if os.path.exists(process_path + "RunWeb"):
                    os.remove(process_path + "RunWeb")

            ##############################
            ### CONVERT DELPHES OUTPUT ###
            ##############################
            
            ### If the lhco file does not exist already, then create one looking for the root file
            if not(os.path.exists(lhco_file_path)):
            
                ### Get latest .root event file
                root_file_list = sorted(glob.glob(process_path + "Events/" + parameter_space_point + "/*.root"))
                last_root_file = root_file_list[len(root_file_list)-1]
                
                if not(os.path.exists(output_folder_events_lhco)):
                    os.mkdir(output_folder_events_lhco)
                command = path_Madgraph + "Delphes/root2lhco " + last_root_file + " " + lhco_file_path
                os.system(command)
            
            ####################
            ## STORE RESULTS ###
            ####################

            ### Store the results in a list with members: (gq, gxi, mZpr [GeV], mDM [GeV], xsection [fb])

            ### Get latest pythia8 .log file
            log_file_list = sorted(glob.glob(process_path + "Events/" + parameter_space_point + "/*pythia8.log"))
            last_log_file = log_file_list[len(log_file_list)-1]

            pythia_output = open(last_log_file, "r")
            text = pythia_output.read()
            pythia_output.close()

            xsection_line = re.findall("^.*Inclusive cross section:.*$", text, re.MULTILINE)[0]
            xsection = float(xsection_line.split()[3]) * pow(10,12) ### conversion from mb to fb
            
            if (mediator_type == 2):
                results.append([couplings.gVd11, couplings.gVu11, couplings.gVXd, masses.MY1, masses.MXd, float(format(xsection, ".2f"))])
            elif (mediator_type == 3):
                results.append([couplings.gAd11, couplings.gAu11, couplings.gAXd, masses.MY1, masses.MXd, float(format(xsection, ".2f"))])
            elif (mediator_type == 4 or mediator_type == 6):
                results.append([str(float(format(couplings.gVd11, ".3f"))), str(float(format(couplings.gVu11, ".3f"))), couplings.gVXd, masses.MY1, masses.MXd, float(format(xsection, ".2f"))])
            elif (mediator_type == 5 or mediator_type == 7):
                results.append([str(float(format(couplings.gVd11, ".3f"))), str(float(format(couplings.gVu11, ".3f"))), couplings.gAXd, masses.MY1, masses.MXd, float(format(xsection, ".2f"))])
            elif (mediator_type == 8):
                results.append([couplings.gVd11, couplings.gVu11, couplings.gVXd, masses.MY1, masses.MXd, float(format(xsection, ".2f"))])
            
            #######################
            ### EVENTS ANALYSIS ###
            #######################

            if not(os.path.exists(output_folder_analysed_events)):
                os.mkdir(output_folder_analysed_events)

            output_filename = parameter_space_point + ".dat"
            output_path = output_folder_analysed_events + output_filename
            
            events = read_lhco(lhco_file_path)

            if not(run.nevents == len(events)):
                sys.exit("Mismatch between generated number of events and Delphes output number of events\n")

            print("\n")
            print("###############")
            print("### SUMMARY ###")
            print("###############")
            print("Generated number of events = " + str(run.nevents))
            print("Total XS = " + str(xsection) + " fb")
            if flag_generate_events:
                print("Elapsed time = " + str(elapsed_time.seconds) + " s")
            print("\n")

            efficiencies_process = events_analysis(events, xsection, output_path)
            efficiencies.append(efficiencies_process)

            ### Remove the Madgraph specific Event folder to free space
            if os.path.exists(process_path + "Events/" + parameter_space_point):
                shutil.rmtree(process_path + "Events/" + parameter_space_point)

    ##########################
    ### WRITE SCAN SUMMARY ###
    ##########################
    
    scan_summary(results, efficiencies, output_folder_analysed_events)

    print("\n")
    print("#####################################")
    print("Delphes events are stored in the folder:")
    print(output_folder_events_lhco)
    print("Analysed events are stored in the folder:")
    print(output_folder_analysed_events)
    print("Experimental analysis summary is in the file:")
    print(output_folder_analysed_events + "scan_summary.dat")
    print("#####################################")


############
### PLOT ###
############

if not(os.path.exists(output_folder_analysed_events + "scan_summary.csv")):
    sys.exit("Cannot generate plot.\nOutput file '" + output_folder_analysed_events + "scan_summary.csv' is missing.\nRun the analysis first.")

plot_results(mZpr_min, mZpr_max, mZpr_bin, output_folder_analysed_events)
