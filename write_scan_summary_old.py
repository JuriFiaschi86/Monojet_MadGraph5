#! /usr/bin/python3

import math
import numpy

### Monojet signal regions 95% CL upper limits on the number of signal events and on visible cross section
### arXiv:2102.10874 - Table 9

#SR_limits_XS = [736., 296., 150., 86., 52., 21., 10., 4.1, 2.1, 1.2, 1.3, 0.5, 0.3]

SR_predicted_events = [1783000, 753000, 314000, 140100, 101600, 29200, 10000, 3870, 1640, 754, 359, 182, 218]
SR_predicted_events_1sigma = [26000, 9000, 3500, 1600, 1200, 400, 180, 80, 40, 20, 10, 6, 9]
SR_observed_events = [1791624, 752328, 313912, 141036, 102888, 29458, 10203, 3986, 1663, 738, 413, 187, 207]

Lum = 139
conversion_1sigma_to_95CL = 1.96

#### Signal systematic uncertainties
#experimental_sys = 4/100 ### reconstruction, energy scales and resolutions
#lum_sys = 1.7/100 ### luminosity uncertainty
#acceptance_sys = 5/100 ### modeling of the initial- and final-state radiation
#PDF_choice_sys = 10/100 ### choice of different PDF sets
#scales_acceptance_sys = 10/100 ### scale variation on acceptance for vector mediator
#scales_XS_sys = 10/100 ### scale variation on cross section
#PDF_XS_sys = 5/100 ### PDF error on cross section for vector mediator

#total_sys = experimental_sys + lum_sys + acceptance_sys + PDF_choice_sys + scales_acceptance_sys + scales_XS_sys + PDF_XS_sys


### Signal systematic uncertainties
experimental_sys = numpy.array([1/100, 7/100]) ### reconstruction, energy scales and resolutions
lum_sys = numpy.array([1.7/100, 1.7/100]) ### luminosity uncertainty
acceptance_sys = numpy.array([3/100, 6/100]) ### modeling of the initial- and final-state radiation
PDF_choice_sys = numpy.array([10/100, 10/100]) ### choice of different PDF sets
scales_acceptance_sys = numpy.array([15/100, 15/100]) ### scale variation on acceptance for vector mediator
scales_XS_sys = numpy.array([10/100, 10/100]) ### scale variation on cross section
PDF_XS_sys = numpy.array([5/100, 5/100]) ### PDF error on cross section for vector mediator

total_sys_1 = numpy.array([experimental_sys, lum_sys, acceptance_sys, PDF_choice_sys, scales_acceptance_sys, scales_XS_sys, PDF_XS_sys]).sum(axis = 0)
total_sys_2 = numpy.array([experimental_sys, lum_sys, acceptance_sys, PDF_choice_sys, scales_XS_sys, PDF_XS_sys]).sum(axis = 0)


def scan_summary(results, efficiencies, folder):
    
    
    text = ""
    text += "###########################" + "\n"
    text += "### SUMMARY OF THE SCAN ###" + "\n"
    text += "###########################" + "\n"
    
    text += "gq\tgxi\tmZpr [GeV]\tmDM [GeV]\tXS [fb]\tXS(SR0) [fb]\tSRexcluded1\tSRexcluded2" + "\n"
    for i in range(len(results)):
        SR_check_1 = ""
        SR_check_2 = ""
        text += str(results[i][0]) + "\t" + str(results[i][1]) + "\t" + str(results[i][2]) + "\t\t" + str(results[i][3]) + "\t\t" + str(results[i][4]) + "\t\t" + format(results[i][4] * efficiencies[i][0], ".2f") + "\t\t"
        
        for j in range(len(efficiencies[i])):
            
            stat_signal = results[i][4] * efficiencies[i][j] * Lum
            Delta_stat_signal = math.sqrt(stat_signal)
            
            ### Signal systematic with acceptance scale variation systematic (linear interpolation between SRs)
            signal_SR_systematic_1 = total_sys_1[0] + (total_sys_1[1] - total_sys_1[0]) * (j/(len(efficiencies[i])-1))
            ### Signal systematic w/o acceptance scale variation systematic (linear interpolation between SRs)
            signal_SR_systematic_2 = total_sys_2[0] + (total_sys_2[1] - total_sys_2[0]) * (j/(len(efficiencies[i])-1))
                        
            Delta_sys_signal_1 = signal_SR_systematic_1 * stat_signal
            Delta_sys_signal_2 = signal_SR_systematic_2 * stat_signal
            
            ### Calculate 95% CL upper bound on number of signal events adding in quadrature signal systematic, background systematic+statistic, signal statistic
            exclusion_95CL_1 = math.sqrt(Delta_sys_signal_1**2 + (SR_predicted_events_1sigma[j]**2 + Delta_stat_signal**2)) * conversion_1sigma_to_95CL
            exclusion_95CL_2 = math.sqrt(Delta_sys_signal_2**2 + (SR_predicted_events_1sigma[j]**2 + Delta_stat_signal**2)) * conversion_1sigma_to_95CL
            
            ### Exclusion check w/o considering observed events
            exclusion_check_1 = stat_signal > exclusion_95CL_1
            exclusion_check_2 = stat_signal > exclusion_95CL_2
            
            #### Exclusion check with observed events
            #exclusion_check_1 = abs((stat_signal + SR_predicted_events[j]) - SR_observed_events[j]) > exclusion_95CL_1
            #exclusion_check_2 = abs((stat_signal + SR_predicted_events[j]) - SR_observed_events[j]) > exclusion_95CL_2


            if exclusion_check_1:
                SR_check_1 += str(j) + ","
            if exclusion_check_2:
                SR_check_2 += str(j) + ","
        if not(SR_check_1): SR_check_1 = "-1" ### if the signal is not excluded in any SR, flag it with "-1"
        else: SR_check_1 = SR_check_1[:-1]
        if not(SR_check_2): SR_check_2 = "-1" ### if the signal is not excluded in any SR, flag it with "-1"
        else: SR_check_2 = SR_check_2[:-1]
        
        text += SR_check_1 + "\t\t" + SR_check_2
        text += "\n"
        
    output = folder + "scan_summary.dat"
    ### Write summary to file
    output_file = open(output, "w")
    output_file.write(text)
    output_file.close()
