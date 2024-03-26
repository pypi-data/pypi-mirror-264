"""Module for making plot with two 1D Histograms and their ratio."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import types
import pandas as pd
from atlasify import atlasify
from atlasify import monkeypatch_axis_labels
monkeypatch_axis_labels()

# Import own utility functions
import niceplot.utils as utils

def draw1dratio(
    dfdict: dict[pd.DataFrame],
    denominator: str,
    numerator: str,
    x: str,
    range: list,
    nbins: int,
    xlab: str = None,
    ylab: str = "events",
    denomlab: str = None,
    numlab: str = None,
    suffix: str = "",
    addinfo: str = "",
    logy: bool = False,
    output_dir: str = None
  ) -> None:
  """Function to draw two 1d histograms and their ratio, both including statistical uncertainties."""
  
  # Replace x-axis label by nice string if custom xlab is not provided:
  xlab = utils.getnicestr(x) if xlab == None else xlab
  fig, (ax_top, ax_bottom) = plt.subplots(nrows=2, ncols=1, height_ratios=[1.5,1])
  
  # Get denominator and numerator:
  x_den = dfdict[denominator][x]
  x_num = dfdict[numerator][x]
  
  # If range is not provided, take min/max of the two histograms:
  if range == None:
    minval = min(min(x_den.values), min(x_num.values))
    maxval = max(max(x_den.values), max(x_num.values))
    range = [minval, maxval]

  # Get automatic nbins if value is not provided:
  nbins = nbins if nbins != None else 50
  
  # Make histograms and bar plots for errors:
  hist_num, bins, _ = ax_top.hist(x_num, bins=nbins, range=range, label=numlab, histtype='step')
  bincenters = bins[:-1]+np.diff(bins)[0]/2.
  band_num = ax_top.bar(bincenters, height=2*np.sqrt(hist_num), bottom=(hist_num-np.sqrt(hist_num)), width=np.diff(bins), alpha=0.5, facecolor='tab:blue')
  hist_den, _, _ = ax_top.hist(x_den, bins=nbins, range=range, label=denomlab, histtype='step')
  band_denom = ax_top.bar(bincenters, height=2*np.sqrt(hist_den), bottom=(hist_den-np.sqrt(hist_den)), width=np.diff(bins), alpha=0.5, facecolor='tab:orange')

  # Fixing legend to include uncertainty by creating new legend handles but use the colors from the existing ones
  handles, labels = ax_top.get_legend_handles_labels()
  new_handles = [Line2D([], [], c=h.get_edgecolor()) for h in handles]
  ax_top.legend(handles=[(new_handles[0], band_num), (new_handles[1], band_denom)] , labels=labels, loc='upper right')

  # Make ratio and error:  
  ratio, ratioerr = utils.saferatio(hist_num, hist_den)
  ax_bottom.errorbar(bincenters, ratio, yerr=ratioerr, fmt='ko', label='ratio', markersize=4)
  
  if logy:
    ax_top.set_yscale('log')
    ax_top.set_ylim(1., 2*max( [max(hist_den), max(hist_num)]) )
  else:
    ax_top.set_ylim(1., max( [max(hist_den), max(hist_num)]) )
  
  # Set labels and limits for axes:
  ax_top.set_ylabel(ylab, fontsize=13)
  ax_top.axes.xaxis.set_ticklabels([])
  ax_bottom.set_xlabel(xlab, fontsize=13)
  ax_bottom.set_ylabel('ratio', fontsize=13)
  ax_bottom.set_xlim(ax_top.get_xlim())
  ax_bottom.set_ylim(0., max(ratio))
  
  # Correct offset for potential exponential on x and y axes; fix layout:
  ax_top.yaxis._update_offset_text_position = types.MethodType(utils.top_offset, ax_top.yaxis)
  ax_bottom.xaxis._update_offset_text_position = types.MethodType(utils.bottom_offset, ax_bottom.xaxis)
  fig.tight_layout(rect=(0, 0, 1, 0.94)) # default: left=0, bottom=0, right=1, top=1
  
  # ATLAS Label:
  if addinfo == "":
    atlasify("Internal", outside=True, axes=ax_top) 
  else:
    atlasify("Internal", addinfo, outside=True, axes=ax_top) 
  atlasify(False, axes=ax_bottom)
  
  # Save:
  return utils.savefile(fig, output_dir, f'1dratio_{x}_{suffix}.pdf')
