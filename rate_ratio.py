#!/usr/bin/env python

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, AutoMinorLocator, ScalarFormatter
import matplotlib.patheffects as pe
import numpy as np
from scipy.optimize import minimize
from sys import exit


plt.rc('font',**{'family':'serif','serif':['Computer Modern Roman'], 'size':11})
plt.rc('legend',**{'fontsize':10,'labelspacing':0.3})
plt.rc('text', usetex=True)

plt.rcParams['text.latex.preamble'] = r'\usepackage{siunitx} \usepackage{amsmath} \usepackage{mathrsfs}'

def fmtLog10(x, pos):
    'The two args are the value and tick position'
    ex = np.log10(x)
    def fmt( ex ):
      if ex == 0: return r'$1$'
      elif ex == -1: return r'$0.1$'
      elif ex == 1: return r'$10$'
      else: return r'$10^{%d}$'%ex
    return fmt(ex)

def fmtneg(x, pos):
    ex = np.log10(x)
    return r'$-10^{%d}$'%ex

formatter = FuncFormatter(fmtLog10)
##formatneg = FuncFormatter(fmtneg)

# ---------------------------------------------------------------------------- #
#   Import the lists from MMA
# ---------------------------------------------------------------------------- #
x1, y1 = np.loadtxt( "rate/rate_ratio.dat", unpack = True )
#x2, y2 = np.loadtxt( "rate/rate_pion_average.dat", unpack = True )
#x3, y3 = np.loadtxt( "rate/rate_pion_average.dat", unpack = True )

ord1 = np.argsort(x1)
#ord2 = np.argsort(x2)
#ord3 = np.argsort(x3)
#jbx, jby, jbz, jbr = np.loadtxt( "./joachim/Plot_AA_uds_pmm_Xe.dat", unpack = True )

##COL1 = '#3d9cff'
COL1 = 'royalblue'
COL2 = '#4bcc49'
COL3 = '#ffb600'
COL4 = '#ff1116'

fig, ax1 = plt.subplots()

ax1.set_xlim(-1.5,1.5)
ax1.set_ylim(0.9,1.3)
xticks = np.arange(-1.5,1.6,0.5)
ax1.set_xticks( xticks )
y1ticks = [1.0,1.1,1.2,1.3]
ax1.set_yticks( y1ticks )
##ax1.set_yticklabels( y1ticks )
#ax1.set_yscale('log')
# -------------------------------------------------------------------- #
#  Set axis labels
# -------------------------------------------------------------------- #
ax1.set_ylabel(r'$\mathcal{R}_\text{no l.m.}/\mathcal{R}_\text{l.m.}$')
ax1.set_xlabel(r'${\mathscr{C}}_{2,d}^{(6)}/{\mathscr{C}}_{2,u}^{(6)}$')
#ax1.yaxis.set_label_coords(-0.2, 0.5)

ax1.text(0.95,0.05,r'Xenon', #; $\mathcal{C}_{4,u}^{(6)}=0$',\
    {'ha':'right','va':'bottom'}, transform=ax1.transAxes, fontsize=10)#,
# -------------------------------------------------------------------- #
#  Set axis ticks
# -------------------------------------------------------------------- #
ax1.tick_params(which='both',direction='in', top='on', right='on', bottom='off')
#ax1.yaxis.set_major_formatter(formatter)
ax1.yaxis.set_minor_formatter(formatter)
#ax1.yaxis.set_minor_locator( AutoMinorLocator(5) )

# -------------------------------------------------------------------- #
#  
# -------------------------------------------------------------------- #
ax1.plot( x1[ord1], y1[ord1], lw=1.2, color='0.5',
    # label=r'without light meson contributions',
          dash_capstyle='round')
#ax1.plot( x2[ord2], y2[ord2], lw=1.2, color=COL1,ls='--',
#    label=r'with light meson contributions', dash_capstyle='round')
# ax1.plot( x3[ord3], y3[ord3], lw=1.2, color=COL4,ls=':',
#     label=r'$A\cdot A$ only', dash_capstyle='round')
ax1.grid(ls=':',c='0.7')
# -------------------------------------------------------------------- #
#  Format the legend
# -------------------------------------------------------------------- #
#ax1.legend()
leg = ax1.legend( ##curves, labels, ##loc=(0.5,0.4), 
    handlelength=1.5, fontsize=10, #bbox_to_anchor=(0.5,1),
    loc='lower left', framealpha=0)#, borderpad=0.02)# , loc=4) 
##leg.legendPatch.set_lw(0.0)
##leg.legendPatch.set_edgecolor('w')

# -------------------------------------------------------------------- #
#  Automatically calculate the canvas size
# -------------------------------------------------------------------- #
# Margins
PW = 8.0; PH = 6.0;
LM = 1.75; RM = 0.35;
BM = 1.45; TM = 0.45;
CW = PW+LM+RM; CH = PH+BM+TM;

adjustprops = dict(left=LM/CW, bottom=BM/CH, right=(1.-RM/CW), top=(1.-TM/CH), hspace=0)
fig.set_size_inches( CW/2.54, CH/2.54 )
fig.subplots_adjust(**adjustprops)
fig.savefig('rate_ratio.pdf')
