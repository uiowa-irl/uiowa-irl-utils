"""Functions for plotting curves."""

import matplotlib.pyplot as plt
import numpy as np

import os
import json
import argparse
import numpy as np
import pandas as pd 
from pylab import exp
import matplotlib as mpl
import scipy.stats as ss
from matplotlib import mlab
from tabulate import tabulate
import matplotlib.pyplot as plt
from  pprint import pprint as pp
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)


"""
Description: A wrapper to plot minimal box plots

Documentation: https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.pyplot.boxplot.html#matplotlib.pyplot.boxplot

matplotlib.pyplot.boxplot(x, notch=None, sym=None, vert=None, whis=None, positions=None, widths=None, patch_artist=None, bootstrap=None, usermedians=None, conf_intervals=None, meanline=None, showmeans=None, showcaps=None, showbox=None, showfliers=None, boxprops=None, labels=None, flierprops=None, medianprops=None, meanprops=None, capprops=None, whiskerprops=None, manage_ticks=True, autorange=False, zorder=None, *, data=None)
"""
def plotBox( data=[], title="", xlabel="", ylabel=""):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.boxplot(data)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax

def plotBar(x_seq, title="", xlabel="", ylabel=""):
    width=len(x_seq)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(width, x_seq)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return ax
            
