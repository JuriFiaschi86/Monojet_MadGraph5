#! /usr/bin/python3

import os
import sys

maxjetpt_cut = 150.
met_cut = 200.
energeticjet_cut = 30.
energeticjet_number_cut = 4

### MET cuts for exclusive signal regions 1 to 12
met_cut_SR0 = [met_cut, 250.]
met_cut_SR1 = [250., 300.]
met_cut_SR2 = [300., 350.]
met_cut_SR3 = [350., 400.]
met_cut_SR4 = [400., 500.]
met_cut_SR5 = [500., 600.]
met_cut_SR6 = [600., 700.]
met_cut_SR7 = [700., 800.]
met_cut_SR8 = [800., 900.]
met_cut_SR9 = [900., 1000.]
met_cut_SR10 = [1000., 1100.]
met_cut_SR11 = [1100., 1200.]
met_cut_SR12 = [1200., 13000.]

def read_lhco(file_path):
    
    count_events = 0
    event = []
    total_events = []
    
    with open(file_path) as fp:
        for line in fp:
            row = line.split()
            if (row[0] == "#"): continue
            if (row[0] == "0"):
                count_events += 1
                total_events.append(event)
                event = []
                continue
            event.append([int(row[0]), int(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5])])
    
    total_events.append(event) ### append the last event
    total_events.pop(0)
    
    if not(count_events == len(total_events)):
        sys.exit("Mismatch between generated number of events and read number of events in .lhco file\n")
    else: return(total_events)


def events_analysis(events, xsection, output):    
    
    nevent = 0
    
    selection_maxjetpt = 0
    selection_maxjetpt_events = []
    selection_met = 0
    selection_met_events = []
    selection_nenergeticjets = 0
    selection_nenergeticjets_events = []
    selection_delta_phi = 0
    selection_delta_phi_events = []
    
    selection_total = 0
    selection_total_events = []
    
    njet_event = []
    maxjetpt_event = []
    met_event = []
    
    selection_met_SR0 = 0
    selection_met_SR1 = 0
    selection_met_SR2 = 0
    selection_met_SR3 = 0
    selection_met_SR4 = 0
    selection_met_SR5 = 0
    selection_met_SR6 = 0
    selection_met_SR7 = 0
    selection_met_SR8 = 0
    selection_met_SR9 = 0
    selection_met_SR10 = 0
    selection_met_SR11 = 0
    selection_met_SR12 = 0
    
    text = ""
    
    for event in events:
        
        nevent += 1
        
        njets = 0
        nenergeticjets = 0
        maxjetpt = 0
        met = 0
        jetpt = []
        
        maxjetpt_index = 0
        met_index = 0
        
        phi_maxptjet = 0
        phi_met = 0
        delta_phi = 0
        
        #maxjetpt_test = 0
        
        for particle in event:
            if (particle[1] == 4):
                njets += 1
                jetpt.append(particle[4])
                if not(maxjetpt_index): ### the jets are already ordered from the most energetic
                    maxjetpt_index = particle[0]
                if (particle[4] > energeticjet_cut):
                    nenergeticjets += 1
            if (particle[1] == 6):
                met_index = particle[0]
                
        if njets:
            maxjetpt = max(jetpt)
            met = sum(jetpt)
            
            phi_maxptjet = event[maxjetpt_index-1][3]
            phi_met = event[met_index-1][3]
            delta_phi = abs(phi_maxptjet - phi_met)
            
        delta_phi_cut = 0
        if (met >= 250.):
            delta_phi_cut = 0.4
        elif (met > 200.):
            delta_phi_cut = 0.6
        
        #if (maxjetpt_test == maxjetpt):
            #print("everything ok")
        #else:
            #print("not ok")
        
        njet_event.append(njets)
        maxjetpt_event.append(maxjetpt)
        met_event.append(met)
        
        if (maxjetpt > maxjetpt_cut):
            selection_maxjetpt += 1
            selection_maxjetpt_events.append(nevent)
        
        if (nenergeticjets < energeticjet_number_cut):
            selection_nenergeticjets += 1
            selection_nenergeticjets_events.append(nevent)
        
        if (met > met_cut):
            selection_met += 1
            selection_met_events.append(nevent)
        
        if (delta_phi >= delta_phi_cut):
            selection_delta_phi += 1
            selection_delta_phi_events.append(nevent)
    
        if ((maxjetpt > maxjetpt_cut) and (met > met_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_total += 1
            selection_total_events.append(nevent)
        
        ### Efficiencies for signal regions
        if (((met > met_cut_SR0[0]) and (met <= met_cut_SR0[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR0 += 1
        if (((met > met_cut_SR1[0]) and (met <= met_cut_SR1[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR1 += 1
        if (((met > met_cut_SR2[0]) and (met <= met_cut_SR2[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR2 += 1
        if (((met > met_cut_SR3[0]) and (met <= met_cut_SR3[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR3 += 1
        if (((met > met_cut_SR4[0]) and (met <= met_cut_SR4[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR4 += 1
        if (((met > met_cut_SR5[0]) and (met <= met_cut_SR5[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR5 += 1
        if (((met > met_cut_SR6[0]) and (met <= met_cut_SR6[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR6 += 1
        if (((met > met_cut_SR7[0]) and (met <= met_cut_SR7[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR7 += 1
        if (((met > met_cut_SR8[0]) and (met <= met_cut_SR8[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR8 += 1
        if (((met > met_cut_SR9[0]) and (met <= met_cut_SR9[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR9 += 1
        if (((met > met_cut_SR10[0]) and (met <= met_cut_SR10[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR10 += 1
        if (((met > met_cut_SR11[0]) and (met <= met_cut_SR11[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR11 += 1
        if (((met > met_cut_SR12[0]) and (met <= met_cut_SR12[1])) and (maxjetpt > maxjetpt_cut) and (nenergeticjets < energeticjet_number_cut) and (delta_phi >= delta_phi_cut)):
            selection_met_SR12 += 1
        
    ### Implement at least 1 event for upper limit on the efficiency
    if not(selection_met_SR0): selection_met_SR0 = 1
    if not(selection_met_SR1): selection_met_SR1 = 1
    if not(selection_met_SR2): selection_met_SR2 = 1
    if not(selection_met_SR3): selection_met_SR3 = 1
    if not(selection_met_SR4): selection_met_SR4 = 1
    if not(selection_met_SR5): selection_met_SR5 = 1
    if not(selection_met_SR6): selection_met_SR6 = 1
    if not(selection_met_SR7): selection_met_SR7 = 1
    if not(selection_met_SR8): selection_met_SR8 = 1
    if not(selection_met_SR9): selection_met_SR9 = 1
    if not(selection_met_SR10): selection_met_SR10 = 1
    if not(selection_met_SR11): selection_met_SR11 = 1
    if not(selection_met_SR12): selection_met_SR12 = 1
    
    efficiencies = [selection_met_SR0/nevent, selection_met_SR1/nevent, selection_met_SR2/nevent, selection_met_SR3/nevent, selection_met_SR4/nevent, selection_met_SR5/nevent, selection_met_SR6/nevent, selection_met_SR7/nevent, selection_met_SR8/nevent, selection_met_SR9/nevent, selection_met_SR10/nevent, selection_met_SR11/nevent, selection_met_SR12/nevent]
    
    
    text += "event#\t#jets\t    MET\t    maxPTjet\n"
    for survived_event in selection_total_events:
        text += str(survived_event) + "\t" + str(njet_event[survived_event-1]) + "\t" + "{:10.2f}".format(met_event[survived_event-1]) + "\t" + "{:10.2f}".format(maxjetpt_event[survived_event-1])+ "\n"
    
    text += "\n"
    text += "#####################################" + "\n"
    text += "### SUMMARY OF THE SELECTION CUTS ###" + "\n"
    text += "#####################################" + "\n"
    text += "XS (before cuts) [fb] : " "{:.2f}".format(xsection) + "\n"
    text += "Events surviving maxjetPT > " + str(maxjetpt_cut) + " GeV : " + str(selection_maxjetpt) + "/" + str(nevent) + "\n"
    text += "Events surviving # energetic (pT > " + str(energeticjet_cut) + " GeV) jets < " + str(energeticjet_number_cut) + " : " + str(selection_nenergeticjets) + "/" + str(nevent) + "\n"
    text += "Events surviving MET > " + str(met_cut) + " GeV : " + str(selection_met) + "/" + str(nevent) + "\n"
    text += "Events surviving delta_phi > 0.4(0.6) : " + str(selection_delta_phi) + "/" + str(nevent) + "\n"
    text += "Events surviving all selection cuts : " + str(selection_total) + "/" + str(nevent) + "\n"
    text += "#####################################" + "\n"
    
    for i in range(len(efficiencies)):
        text += "Efficiency SR" + str(i) + " : " + "{:10.5f}".format(efficiencies[i]) + "\n"
    text += "#####################################" + "\n"
    
    ### Write surviving events and efficiencies results
    output_file = open(output, "w")
    output_file.write(text)
    output_file.close()
    
    print("#####################################")
    print("### SUMMARY OF THE SELECTION CUTS ###")
    print("#####################################")
    print("Events surviving maxjetPT > " + str(maxjetpt_cut) + " GeV : " + str(selection_maxjetpt) + "/" + str(nevent))
    print("Events surviving # energetic (pT > " + str(energeticjet_cut) + " GeV) jets < " + str(energeticjet_number_cut) + " : " + str(selection_nenergeticjets) + "/" + str(nevent))
    print("Events surviving MET > " + str(met_cut) + " GeV : " + str(selection_met) + "/" + str(nevent))
    print("Events surviving delta_phi > 0.4(0.6) : " + str(selection_delta_phi) + "/" + str(nevent))
    print("Events surviving all selection cuts : " + str(selection_total) + "/" + str(nevent))
    print("")
    
    return efficiencies
