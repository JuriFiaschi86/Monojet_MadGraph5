#! /usr/bin/python3

import os

def write_madevent_shell(process):
    
    current_dir = os.getcwd() + "/"
    
    text = ""
    text += "set automatic_html_opening False"
    text += "\n"
    text += "launch " + process + " --multicore --nb_core=8"
    text += "\n"
    text += " shower=Pythia8"
    text += "\n"
    text += " detector=Delphes"
    text += "\n"
    text += " analysis=OFF"
    text += "\n"
    text += "quit"    
    
    shell_file = open(current_dir + "madevent_shell.sh", "w")
    shell_file.write(text)
    shell_file.close()
