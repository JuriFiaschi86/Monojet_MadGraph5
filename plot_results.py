#! /usr/bin/python3

import numpy
import pandas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def plot_results(mZpr_min, mZpr_max, mZpr_bin, output_folder):
    
    ### Read data from csv file
    data = pandas.read_csv(output_folder + "scan_summary.csv", delimiter = ";")
    
    ### matplotlib settings
    matplotlib.rc("figure", dpi=600)
    matplotlib.rc("savefig", pad_inches=0)
    matplotlib.rc("xtick.minor", visible=True)
    matplotlib.rc("ytick.minor", visible=True)
    matplotlib.rc("axes.formatter", useoffset=False)
    
    ### Plot axes
    plt.figure()
    plt.title(r"Monojet exclusion 95% CL")
    plt.xlabel(r"$m_{\mathrm{Z^\prime}}$ [GeV]")
    plt.ylabel(r"$m_{\mathrm{DM}}$ [GeV]")
    plt.xscale("linear")
    plt.yscale("linear")
    plt.xlim([mZpr_min, mZpr_max])
    plt.ylim([0, mZpr_max/2])
    
    limits_1 = pandas.DataFrame(columns=["mZpr [GeV]", "mDM [GeV]"])
    limits_2 = pandas.DataFrame(columns=["mZpr [GeV]", "mDM [GeV]"])

    ### Get the exclusion limit as the intermediate point between first excluded and first allowed (Exclusion 1)
    mZpr = mZpr_min
    i = 0
    while mZpr <= mZpr_max:
    
        temp = data.loc[data["mZpr [GeV]"] == mZpr].reset_index()
        index_list = numpy.array(temp.index[temp["SRexcluded1"] == "-1"].tolist())
                
        if not(len(index_list)):
            mZpr += mZpr_bin
            continue
        index = min(index_list)
        
        if not(index):
            mZpr += mZpr_bin
            continue
        
        limits_1.at[i, "mZpr [GeV]"] = mZpr
        limits_1.at[i, "mDM [GeV]"] = (temp.iloc[index]["mDM [GeV]"] + temp.iloc[index-1]["mDM [GeV]"])/2
        
        i += 1
        mZpr += mZpr_bin
    
    plt.plot(limits_1["mZpr [GeV]"], limits_1["mDM [GeV]"], color = "black", linestyle= "solid", label = "with scale uncertainty on acceptance")
    
    ### Get the exclusion limit as the intermediate point between first excluded and first allowed (Exclusion 2)
    mZpr = mZpr_min
    i = 0
    while mZpr <= mZpr_max:
    
        temp = data.loc[data["mZpr [GeV]"] == mZpr].reset_index()
        index_list = numpy.array(temp.index[temp["SRexcluded2"] == "-1"].tolist())
                
        if not(len(index_list)):
            mZpr += mZpr_bin
            continue
        index = min(index_list)
        
        if not(index):
            mZpr += mZpr_bin
            continue
        
        limits_2.at[i, "mZpr [GeV]"] = mZpr
        limits_2.at[i, "mDM [GeV]"] = (temp.iloc[index]["mDM [GeV]"] + temp.iloc[index-1]["mDM [GeV]"])/2
        
        i += 1
        mZpr += mZpr_bin
    
    plt.plot(limits_2["mZpr [GeV]"], limits_2["mDM [GeV]"], color = "black", linestyle= "dashed", label = "w/o scale uncertainty on acceptance")
    
    plt.legend()
    plot_name = output_folder + "Monojet_exclusion.pdf"
    plt.savefig(plot_name)
    
    ### Write points to file
    output = output_folder + "Monojet_exclusion_1.dat"
    with open(output,"w") as outfile:
        limits_1.to_string(outfile, index=None)
    ### Write points to file
    output = output_folder + "Monojet_exclusion_2.dat"
    with open(output,"w") as outfile:
        limits_2.to_string(outfile, index=None)
        
    print("\n")
    print("#####################################")
    print("Plot saved in:")
    print(output_folder + "Monojet_exclusion.pdf")
    print("#####################################")
    print("\n")
