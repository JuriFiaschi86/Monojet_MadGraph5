#! /usr/bin/python3

import os
import numpy
import math
import pandas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors


Mtarget = 0.939 ### neutron mass


########################
#### MONOJET RESULTS ###
########################

def monojet_limits(process):
    
    current_dir = os.getcwd() + "/"
    monojet_path = current_dir + process + "Monojet_exclusion_2.dat"

    monojet_file = open(monojet_path, "r")
    monojet_file.readline() ### skip first line
    line = monojet_file.readline()

    monojet_limits = pandas.DataFrame(columns=["mZpr [GeV]", "mDM [GeV]"])

    ### Read monojet exclusion
    count = 0
    while True:
        count += 1
    
        # Get next line from file
        line = monojet_file.readline()
        if not line:
            break
        monojet_limits.at[count, "mZpr [GeV]"] = float(line.split()[0])
        monojet_limits.at[count, "mDM [GeV]"] = float(line.split()[1])
    monojet_file.close()
    
    ### Recast limits in SI cross section & Wilson coefficient
    if (not(process.find("vector") == -1)):
        
        ### if the value of gq is specified (i.e. universal couplings to quarks), read the specific value from the folder name
        if (not(process.find("gq") == -1)):
            gq = float(process[process.find("gq")+3:process.find("gxi")-1])
            gxi = float(process[process.find("gxi")+4:process.find("Analysed_Events")-1])
        ### if the value of gq is not specified (i.e. right-handed couplings to quarks), we assume that we have fixed the couplings such that gq = 0.25
        else:
            gq = 0.25
            gxi = 1.0
        
        monojet_SI = []
        for i in range(len(monojet_limits["mDM [GeV]"])):
            monojet_SI.append(6.9 * pow(10,-41) * pow(gq * gxi / 0.25, 2) * pow(1 / (monojet_limits["mZpr [GeV]"].iloc[i] / pow(10,3)),4) * pow((Mtarget * monojet_limits["mDM [GeV]"].iloc[i]/(Mtarget + monojet_limits["mDM [GeV]"].iloc[i])),2))
        monojet_limits["sigmaSI [cm^2]"] = monojet_SI
        
        monojet_c = []
        for i in range(len(monojet_limits["mDM [GeV]"])):
            monojet_c.append(gq * gxi / pow(monojet_limits["mZpr [GeV]"].iloc[i], 2))
        monojet_limits["c [GeV^{-2}]"] = monojet_c
        
        monojet_1oversqrtc = []
        for i in range(len(monojet_limits["c [GeV^{-2}]"])):
            monojet_1oversqrtc.append(1/math.sqrt(monojet_limits["c [GeV^{-2}]"].iloc[i]))
        monojet_limits["1/sqrt(c) [GeV]"] = monojet_1oversqrtc
    
    ### Recast limits in SD cross section & Wilson coefficient
    if (not(process.find("axial") == -1)):
        
        ### if the value of gq is specified (i.e. universal couplings to quarks), read the specific value from the folder name
        if (not(process.find("gq") == -1)):
            gq = float(process[process.find("gq")+3:process.find("gxi")-1])
            gxi = float(process[process.find("gxi")+4:process.find("Analysed_Events")-1])
        ### if the value of gq is not specified (i.e. right-handed couplings to quarks), we assume that we have fixed the couplings such that gq = 0.25
        else:
            gq = 0.25
            gxi = 1.0
        
        monojet_SD = []
        for i in range(len(monojet_limits["mDM [GeV]"])):
            monojet_SD.append(2.4 * pow(10,-42) * pow(gq * gxi / 0.25, 2) * pow(1 / (monojet_limits["mZpr [GeV]"].iloc[i] / pow(10,3)),4) * pow((Mtarget * monojet_limits["mDM [GeV]"].iloc[i]/(Mtarget + monojet_limits["mDM [GeV]"].iloc[i])),2))
        monojet_limits["sigmaSD [cm^2]"] = monojet_SD
        
        monojet_c = []
        for i in range(len(monojet_limits["mDM [GeV]"])):
            monojet_c = gq * gxi / pow(monojet_limits["mZpr [GeV]"].iloc[i], 2)
        monojet_limits["c [GeV^{-2}]"] = monojet_c
        
        monojet_1oversqrtc = []
        for i in range(len(monojet_limits["c [GeV^{-2}]"])):
            monojet_1oversqrtc.append(1/math.sqrt(monojet_limits["c [GeV^{-2}]"].iloc[i]))
        monojet_limits["1/sqrt(c) [GeV]"] = monojet_1oversqrtc
    
    return monojet_limits


#####################
### XENON RESULTS ###
#####################

def xenon_limits():
    
    current_dir = os.getcwd() + "/"
    xenon_path = current_dir + "xenon1t_1ty.csv"

    xenon_limits = pandas.read_csv(xenon_path, delimiter = ",", names = ("mDM [GeV]", "sigmaSI [cm^2]"))

    gq = 0.25
    gxi = 1

    ### Recast limits in mZpr & Wilson coefficient
    xenon_Zpr = []
    for i in range(len(xenon_limits["sigmaSI [cm^2]"])):
        xenon_Zpr.append(pow(6.9 * pow(10,-41) / xenon_limits["sigmaSI [cm^2]"].iloc[i], 0.25) * math.sqrt(gq*gxi/0.25) * math.sqrt(Mtarget * xenon_limits["mDM [GeV]"].iloc[i]/(Mtarget + xenon_limits["mDM [GeV]"].iloc[i])) * pow(10, 3))
    xenon_limits["mZpr [GeV]"] = xenon_Zpr
    
    xenon_c = []
    for i in range(len(xenon_limits["sigmaSI [cm^2]"])):
        xenon_c.append(math.sqrt(xenon_limits["sigmaSI [cm^2]"].iloc[i] / (6.9 * pow(10,-41))) * 0.25 / ((Mtarget * xenon_limits["mDM [GeV]"].iloc[i]/(Mtarget + xenon_limits["mDM [GeV]"].iloc[i]))) * pow(10, -6))
    xenon_limits["c [GeV^{-2}]"] = xenon_c
    
    xenon_1oversqrtc = []
    for i in range(len(xenon_limits["c [GeV^{-2}]"])):
        xenon_1oversqrtc.append(1/math.sqrt(xenon_limits["c [GeV^{-2}]"].iloc[i]))
    xenon_limits["1/sqrt(c) [GeV]"] = xenon_1oversqrtc
    
    return xenon_limits


###################
### LUX RESULTS ###
###################

def lux_limits():
    
    current_dir = os.getcwd() + "/"
    lux_path = current_dir + "LUX_limits.csv"

    lux_limits = pandas.read_csv(lux_path, delimiter = ",", names = ("mDM [GeV]", "sigmaSD [cm^2]"))

    gq = 0.25
    gxi = 1

    ### Recast limits in mZpr & Wilson coefficient
    lux_Zpr = []
    for i in range(len(lux_limits["sigmaSD [cm^2]"])):
        lux_Zpr.append(pow(2.4 * pow(10,-42) / lux_limits["sigmaSD [cm^2]"].iloc[i], 0.25) * math.sqrt(gq*gxi/0.25) * math.sqrt(Mtarget * lux_limits["mDM [GeV]"].iloc[i]/(Mtarget + lux_limits["mDM [GeV]"].iloc[i])) * pow(10, 3))
    lux_limits["mZpr [GeV]"] = lux_Zpr
    
    lux_c = []
    for i in range(len(lux_limits["sigmaSD [cm^2]"])):
        lux_c.append(math.sqrt(lux_limits["sigmaSD [cm^2]"].iloc[i] / (2.4 * pow(10,-42))) * 0.25 / ((Mtarget * lux_limits["mDM [GeV]"].iloc[i]/(Mtarget + lux_limits["mDM [GeV]"].iloc[i]))) * pow(10, -6))
    lux_limits["c [GeV^{-2}]"] = lux_c
    
    lux_1oversqrtc = []
    for i in range(len(lux_limits["c [GeV^{-2}]"])):
        lux_1oversqrtc.append(1/math.sqrt(lux_limits["c [GeV^{-2}]"].iloc[i]))
    lux_limits["1/sqrt(c) [GeV]"] = lux_1oversqrtc
    
    return lux_limits


###################################
### WILSON COEFFICIENTS RESULTS ###
###################################

def wilson_limits_vector():
    
    current_dir = os.getcwd() + "/"
    
    ### Vector mediator XENON1T 1ty exposure limits for r = -0.9
    wilson_coeff_path_vector = current_dir + "xenon1t_1ty_vxi.dat"
    
    wilson_limits_vector = pandas.read_csv(wilson_coeff_path_vector, delimiter = " ", names = ("mDM [GeV]", "c [GeV^{-2}]"))
    
    ### Assume that the limits are computed keeping the magnitude of the couplings to quarks to 0.25, even in the case of purely right handed couplings
    gq = 0.25
    gxi = 1
    
    ### Recast limits in mZpr & sigma SI
    wilson_Zpr_vector = []
    for i in range(len(wilson_limits_vector["c [GeV^{-2}]"])):
        wilson_Zpr_vector.append(math.sqrt(gq * gxi / wilson_limits_vector["c [GeV^{-2}]"].iloc[i]))
    wilson_limits_vector["mZpr [GeV]"] = wilson_Zpr_vector
    
    wilson_SI_vector = []
    for i in range(len(wilson_limits_vector["mDM [GeV]"])):
        wilson_SI_vector.append(6.9 * pow(10,-41) * pow(gq * gxi / 0.25, 2) * pow(1 / (wilson_limits_vector["mZpr [GeV]"].iloc[i] / pow(10,3)),4) * pow((Mtarget * wilson_limits_vector["mDM [GeV]"].iloc[i]/(Mtarget + wilson_limits_vector["mDM [GeV]"].iloc[i])),2))
    wilson_limits_vector["sigmaSI [cm^2]"] = wilson_SI_vector
    
    ### straightfoward 1/sqrt(c)
    wilson_1oversqrtc_vector = []
    for i in range(len(wilson_limits_vector["c [GeV^{-2}]"])):
        wilson_1oversqrtc_vector.append(1/math.sqrt(wilson_limits_vector["c [GeV^{-2}]"].iloc[i]))
    wilson_limits_vector["1/sqrt(c) [GeV]"] = wilson_1oversqrtc_vector
    
    return wilson_limits_vector

def wilson_limits_axial():
    
    current_dir = os.getcwd() + "/"
    
    ### Axial mediator XENON1T 1ty exposure limits for r = +0.05
    wilson_coeff_path_axial = current_dir + "xenon1t_1ty_axi.dat"
    
    wilson_limits_axial = pandas.read_csv(wilson_coeff_path_axial, delimiter = " ", names = ("mDM [GeV]", "c [GeV^{-2}]"))

    ### Assume that the limits are computed keeping the magnitude of the couplings to quarks to 0.25, even in the case of purely right handed couplings
    gq = 0.25
    gxi = 1
    
    ### Recast limits in mZpr & sigma SI??? (or sigmaSD???)
    wilson_Zpr_axial = []
    for i in range(len(wilson_limits_axial["c [GeV^{-2}]"])):
        wilson_Zpr_axial.append(math.sqrt(gq * gxi / wilson_limits_axial["c [GeV^{-2}]"].iloc[i]))
    wilson_limits_axial["mZpr [GeV]"] = wilson_Zpr_axial
    
    wilson_SD_axial = []
    for i in range(len(wilson_limits_axial["mDM [GeV]"])):
        wilson_SD_axial.append(2.4 * pow(10,-42) * pow(gq * gxi / 0.25, 2) * pow(1 / (wilson_limits_axial["mZpr [GeV]"].iloc[i] / pow(10,3)),4) * pow((Mtarget * wilson_limits_axial["mDM [GeV]"].iloc[i]/(Mtarget + wilson_limits_axial["mDM [GeV]"].iloc[i])),2))
    wilson_limits_axial["sigmaSD [cm^2]"] = wilson_SI_axial
    
    ### it is straightfoward to translate into 1/sqrt(c)
    wilson_1oversqrtc_axial = []
    for i in range(len(wilson_limits_axial["c [GeV^{-2}]"])):
        wilson_1oversqrtc_axial.append(1/math.sqrt(wilson_limits_axial["c [GeV^{-2}]"].iloc[i]))
    wilson_limits_axial["1/sqrt(c) [GeV]"] = wilson_1oversqrtc_axial
    
    return wilson_limits_axial


###################
### READ LIMITS ###
###################

process = "right_vector_monojet_gdR_0.177_guR_0.177_gVxi_1_Analysed_Events/"
monojet_limits_1 = monojet_limits(process)

process = "right_vector_monojet_gdR_-0.167_guR_0.186_gVxi_1_Analysed_Events/"
monojet_limits_2 = monojet_limits(process)

process = "axial_monojet_gq_1_gxi_1_Analysed_Events/"
monojet_limits_3 = monojet_limits(process)

xenon_limits = xenon_limits()

lux_limits = lux_limits()


wilson_limits_vector = wilson_limits_vector()


############
## PLOTS ###
############

############################
#### mZpr-mDM plane plot ###
############################

#### matplotlib settings
#matplotlib.rc("figure", dpi=600)
#matplotlib.rc("savefig", pad_inches=0)
#matplotlib.rc("xtick.minor", visible=True)
#matplotlib.rc("ytick.minor", visible=True)
#matplotlib.rc("axes.formatter", useoffset=False)

#### Plot axes
#plt.figure()
##plt.title(r"Monojet exclusion 95% CL")
##plt.title(r"Vector mediator")
#plt.xlabel(r"$m_{\mathrm{Z^\prime}}$ [GeV]")
#plt.ylabel(r"$m_{\mathrm{DM}}$ [GeV]")

#flag_scale = "log"
##flag_scale = "lin"

#if flag_scale == "log":
    #plt.xscale("log")
    #plt.yscale("log")
    #plt.xlim([5, pow(10, 5)])
    #plt.ylim([5, pow(10, 6)])

#if flag_scale == "lin":
    #plt.xscale("linear")
    #plt.yscale("linear")
    #plt.xlim([0, 2700])
    #plt.ylim([0, 1000])

#plt.plot(monojet_limits_1["mZpr [GeV]"], monojet_limits_1["mDM [GeV]"], color = "blue", linestyle= "solid", label = "Monojet r = 1.0")
#plt.plot(monojet_limits_2["mZpr [GeV]"], monojet_limits_2["mDM [GeV]"], color = "blue", linestyle= "dashed", label = "Monojet r = -0.9")
##plt.plot(monojet_limits_3["mZpr [GeV]"], monojet_limits_3["mDM [GeV]"], color = "blue", linestyle= "dotted", label = "Monojet gq = gxi = 1")
#plt.plot(xenon_limits["mZpr [GeV]"], xenon_limits["mDM [GeV]"], color = "red", linestyle= "solid", label = "XENON1T r = 1.0")


#current_dir = os.getcwd() + "/"
#plt.legend()
#plot_name = current_dir + "mZpr_mDM_exclusion.pdf"
#plt.savefig(plot_name)


##########################
#### mDM-SI plane plot ###
##########################

#### matplotlib settings
#matplotlib.rc("figure", dpi=600)
#matplotlib.rc("savefig", pad_inches=0)
#matplotlib.rc("xtick.minor", visible=True)
#matplotlib.rc("ytick.minor", visible=True)
#matplotlib.rc("axes.formatter", useoffset=False)

#### Plot axes
#plt.figure()
#plt.title(r"Vector mediator")
#plt.xlabel(r"$m_{\mathrm{DM}}$ [GeV]")
#plt.ylabel(r"$\sigma_{SI}$ [$cm^2$]")

#plt.xscale("log")
#plt.yscale("log")
#plt.xlim([5, pow(10, 4)])
#plt.ylim([pow(10, -47), pow(10, -34)])

##plt.plot(monojet_limits_3["mDM [GeV]"], monojet_limits_3["sigmaSI [cm^2]"], color = "blue", linestyle= "dotted", label = "Monojet gq = gxi = 1")
#plt.plot(xenon_limits["mDM [GeV]"], xenon_limits["sigmaSI [cm^2]"], color = "red", linestyle= "solid", label = "XENON1T r = 1.0")


#current_dir = os.getcwd() + "/"
#plt.legend()
#plot_name = current_dir + "mDM_SI_exclusion.pdf"
#plt.savefig(plot_name)


##########################
#### mDM-SD plane plot ###
##########################

#### matplotlib settings
#matplotlib.rc("figure", dpi=600)
#matplotlib.rc("savefig", pad_inches=0)
#matplotlib.rc("xtick.minor", visible=True)
#matplotlib.rc("ytick.minor", visible=True)
#matplotlib.rc("axes.formatter", useoffset=False)

#### Plot axes
#plt.figure()
#plt.title(r"Axial mediator")
#plt.xlabel(r"$m_{\mathrm{DM}}$ [GeV]")
#plt.ylabel(r"$\sigma_{SD}$ [$cm^2$]")

#plt.xscale("log")
#plt.yscale("log")
#plt.xlim([5, pow(10, 4)])
#plt.ylim([pow(10, -46), pow(10, -34)])

#plt.plot(monojet_limits_3["mDM [GeV]"], monojet_limits_3["sigmaSD [cm^2]"], color = "blue", linestyle= "dotted", label = "Monojet gq = gxi = 1")
#plt.plot(lux_limits["mDM [GeV]"], lux_limits["sigmaSD [cm^2]"], color = "red", linestyle= "solid", label = "LUX r = 1.0")


#current_dir = os.getcwd() + "/"
#plt.legend()
#plot_name = current_dir + "mDM_SD_exclusion.pdf"
#plt.savefig(plot_name)


#################################
### mDM-C plane plot (Vector) ###
#################################

### matplotlib settings
matplotlib.rc("figure", dpi=600)
matplotlib.rc("savefig", pad_inches=0)
matplotlib.rc("xtick.minor", visible=True)
matplotlib.rc("ytick.minor", visible=True)
matplotlib.rc("axes.formatter", useoffset=False)

### Plot axes
plt.figure()
#plt.title(r"Axial mediator")
plt.xlabel(r"$m_{\mathrm{DM}}$ [GeV]")
plt.ylabel(r"c [$GeV^{-2}$]")

plt.xscale("linear")
plt.yscale("log")
plt.xlim([0, 1200])
plt.ylim([pow(10, -10), pow(10, -3)])

plt.plot(monojet_limits_1["mDM [GeV]"], monojet_limits_1["c [GeV^{-2}]"], color = "blue", linestyle= "solid", label = "Monojet r = 1")
plt.plot(monojet_limits_2["mDM [GeV]"], monojet_limits_2["c [GeV^{-2}]"], color = "blue", linestyle= "dotted", label = "Monojet r = -0.9")
plt.plot(xenon_limits["mDM [GeV]"], xenon_limits["c [GeV^{-2}]"], color = "red", linestyle= "solid", label = "XENON1T r = 1.0")
plt.plot(wilson_limits_vector["mDM [GeV]"], wilson_limits_vector["c [GeV^{-2}]"], color = "red", linestyle= "dotted", label = "XENON1T r = -0.9")

current_dir = os.getcwd() + "/"
plt.legend()
plot_name = current_dir + "mDM_c_vector_exclusion.pdf"
plt.savefig(plot_name)


#################################
#### mDM-C plane plot (Axial) ###
#################################

#### matplotlib settings
#matplotlib.rc("figure", dpi=600)
#matplotlib.rc("savefig", pad_inches=0)
#matplotlib.rc("xtick.minor", visible=True)
#matplotlib.rc("ytick.minor", visible=True)
#matplotlib.rc("axes.formatter", useoffset=False)

#### Plot axes
#plt.figure()
##plt.title(r"Axial mediator")
#plt.xlabel(r"$m_{\mathrm{DM}}$ [GeV]")
#plt.ylabel(r"c [$GeV^{-2}$]")

#plt.xscale("linear")
#plt.yscale("log")
#plt.xlim([0, 1200])
#plt.ylim([pow(10, -8), pow(10, -1)])

#plt.plot(monojet_limits_3["mDM [GeV]"], monojet_limits_3["c [GeV^{-2}]"], color = "blue", linestyle= "dotted", label = "Monojet gq = gxi = 1")
#plt.plot(lux_limits["mDM [GeV]"], lux_limits["c [GeV^{-2}]"], color = "red", linestyle= "solid", label = "LUX r = 1.0")


#current_dir = os.getcwd() + "/"
#plt.legend()
#plot_name = current_dir + "mDM_c_axial_exclusion.pdf"
#plt.savefig(plot_name)


#########################################
### mDM-1/sqrt(C) plane plot (Vector) ###
#########################################

### matplotlib settings
matplotlib.rc("figure", dpi=600)
matplotlib.rc("savefig", pad_inches=0)
matplotlib.rc("xtick.minor", visible=True)
matplotlib.rc("ytick.minor", visible=True)
matplotlib.rc("axes.formatter", useoffset=False)

### Plot axes
plt.figure()
#plt.title(r"Axial mediator")
plt.xlabel(r"$m_{\mathrm{DM}}$ [GeV]")
plt.ylabel(r"1/$\sqrt{c}$ [GeV]")

plt.xscale("linear")
plt.yscale("log")
plt.xlim([0, 1200])
plt.ylim([pow(10, 2), pow(10, 5)])

##plt.plot(monojet_limits_3["mDM [GeV]"], monojet_limits_3["1/sqrt(c) [GeV]"], color = "blue", linestyle= "dotted", label = "Monojet gq = gxi = 1")
#plt.plot(xenon_limits["mDM [GeV]"], xenon_limits["1/sqrt(c) [GeV]"], color = "red", linestyle= "solid", label = "XENON1T r = 1.0")


plt.plot(monojet_limits_1["mDM [GeV]"], monojet_limits_1["1/sqrt(c) [GeV]"], color = "blue", linestyle= "solid", label = "Monojet r = 1")
plt.plot(monojet_limits_2["mDM [GeV]"], monojet_limits_2["1/sqrt(c) [GeV]"], color = "blue", linestyle= "dotted", label = "Monojet r = -0.9")
plt.plot(xenon_limits["mDM [GeV]"], xenon_limits["1/sqrt(c) [GeV]"], color = "red", linestyle= "solid", label = "XENON1T r = 1.0")
plt.plot(wilson_limits_vector["mDM [GeV]"], wilson_limits_vector["1/sqrt(c) [GeV]"], color = "red", linestyle= "dotted", label = "XENON1T r = -0.9")


current_dir = os.getcwd() + "/"
plt.legend()
plot_name = current_dir + "mDM_1oversqrtc_vector_exclusion.pdf"
plt.savefig(plot_name)


#################################
#### mDM-C plane plot (Axial) ###
#################################

#### matplotlib settings
#matplotlib.rc("figure", dpi=600)
#matplotlib.rc("savefig", pad_inches=0)
#matplotlib.rc("xtick.minor", visible=True)
#matplotlib.rc("ytick.minor", visible=True)
#matplotlib.rc("axes.formatter", useoffset=False)

#### Plot axes
#plt.figure()
##plt.title(r"Axial mediator")
#plt.xlabel(r"$m_{\mathrm{DM}}$ [GeV]")
#plt.ylabel(r"1/$\sqrt{c}$ [GeV]")

#plt.xscale("linear")
#plt.yscale("log")
#plt.xlim([0, 1200])
#plt.ylim([pow(10, 1), pow(10, 4)])

#plt.plot(monojet_limits_3["mDM [GeV]"], monojet_limits_3["1/sqrt(c) [GeV]"], color = "blue", linestyle= "dotted", label = "Monojet gq = gxi = 1")
#plt.plot(lux_limits["mDM [GeV]"], lux_limits["1/sqrt(c) [GeV]"], color = "red", linestyle= "solid", label = "LUX r = 1.0")


#current_dir = os.getcwd() + "/"
#plt.legend()
#plot_name = current_dir + "mDM_1oversqrtc_axial_exclusion.pdf"
#plt.savefig(plot_name)
