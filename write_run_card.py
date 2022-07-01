#! /usr/bin/python3

import re
    
def write_param(text, params):
    
    ### Write number of events
    events_line_old = re.findall("^.*nevents.*$", text, re.MULTILINE)[0]
    events_line_new = "  " + str(params.nevents) + events_line_old[7:len(events_line_old)]
    text = text.replace(events_line_old, events_line_new)
    
    ### Write PDF
    pdlabel_line_old = re.findall("^.*pdlabel.*$", text, re.MULTILINE)[0]
    pdlabel_line_new = "     lhapdf" + pdlabel_line_old[12:len(pdlabel_line_old)]
    text = text.replace(pdlabel_line_old, pdlabel_line_new)
    lhaid_line_old = re.findall("^.*lhaid.*$", text, re.MULTILINE)[0]
    lhaid_line_new = "     " + str(params.lhapdfid) + lhaid_line_old[11:len(pdlabel_line_old)] ### corresponds to NNPDF30_lo_as_0118
    text = text.replace(lhaid_line_old, lhaid_line_new)

    ### Write number of events
    scale_line_old = re.findall("^.*dynamical_scale_choice.*$", text, re.MULTILINE)[0]
    scale_line_new = "  " + str(params.scale_choice) + scale_line_old[3:len(scale_line_old)] ### corresponds to user defined ren/fact scales choice
    text = text.replace(scale_line_old, scale_line_new)
    
    return text
    
def write_run_card(path, run):
    
    ### Open and read default param card
    run_template = open(path + "Cards/run_card_default.dat", "r")
    text = run_template.read()
    run_template.close()
    
    text = write_param(text, run)
    
    ### Write run card file
    run_new = open(path + "Cards/run_card.dat", "w")
    run_new.write(text)
    run_new.close()
