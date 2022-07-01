#!/usr/local/bin
import os, sys
from subprocess import call
import subprocess
import fileinput
import os
import random
import re
import sys
import webbrowser
import time
import shutil
import cmath 
#import numpy as np
import array
from array import array
import glob
path = os.getcwd()
from os import remove
from shutil import move
print """
   --------------------------------------------------------- 
   |                 A.Hammad                               | 
   |           HOW TO USE THIS SCRIPT			    |
   | 1- This fille should be run from MadGraph directory    |
   | 2- Make sure that the Number of Events is 1            |
    ---------------------------------------------------------
	 """
time.sleep(10)
model=""
if os.path.exists('output_scan'):
    shutil.rmtree('output_scan')
os.mkdir("output_scan")
if os.path.exists('RunWeb'):
    os.remove('RunWeb')
if os.path.exists('MYfile.sh'):
    os.remove('MYfile.sh')
f = open('MYfile.sh','w+r+x')
f.write("""
#! /bin/sh

   "=========================================="
   "===== NOW YOU ARE MOVING TO MADEVENT======"
   "==========================================" 
  
  set automatic_html_opening False
  launch --multicore --nb_core=4 -f 
""")
f.close()
os.system("chmod -u+xrw MYfile.sh")
files_Veva=glob.glob(path+"/out/*") ##### Here I move to the dir where all spectrum are stored 
for file in files_Veva: ### Scan over all SPheno spectrums in the directory 
    print ('Using  '+str(file))
   
    shutil.copy(file,path+"/Cards/param_card.dat") ## Replace the parameter card in madevent directory by the spheno spectrum
    os.system("./bin/madevent MYfile.sh >/dev/null ") ### run the shell secript 
    #### in the following lines, if you are interested in scanning over the cross section only
    #### then you have to keep the number of events in the run card = 1
    ### as well every time you have to delete the event directory created by madevent for each run
    os.rename(path+"/Events/run_01/run_01_tag_1_banner.txt", path+"/Events/run_01/results_%s"%(str(file[-1:]))) 
    shutil.move(path+"/Events/run_01/results_%s"%(str(file[-1:])) ,  path+"/output_scan/")
    os.system("rm -rf Events/run_01/")
################### read the cross section calculated from madgraph in each run and store it 
f = open(path+'/output_scan/result_plot.dat','w')
f.write('# Hpm_2 \t'+'M_Zp \t'+'total cross section \n')
files_plot=glob.glob(path+'/output_scan/*')
print 'preparing the plot file,...'
time.sleep(10)
for file in files_plot:         ##### I also need to store some of the model parameter beside the cross section
    l = open (file,'r')
    for line in l:
        if str('# Hpm_2') in line:   ### mass of the charged higgs in the model 
            o= line.rsplit()
            h2 = "%0.3E"%float(o[1])
            f.write(h2+'\t')
        if str('# VZp') in line:      ### Zp mass 
            o= line.rsplit()
            h2 = "%0.3E"%float(o[1])
            f.write(h2+'\t')        
        if str('#  Integrated weight (pb)  :') in line:  ## cross section calcualted for each run
            o= line.rsplit()
            h2 = "%0.3E"%float(o[5])
            f.write(h2+'\t')
   
    f.write('\n')         ##break the line to start new event in new line 
f.close()



raw_input("""
        ************************************
          Results are stored in %s/output_scan
          the plot file called "result_plot.dat"
          Please hit any key to exit......
"""%(str(path)))

