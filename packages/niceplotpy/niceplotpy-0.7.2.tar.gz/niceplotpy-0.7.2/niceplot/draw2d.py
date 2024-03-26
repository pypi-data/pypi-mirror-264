"""Module for making 2D Histogram plots."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import types
from atlasify import atlasify
from atlasify import monkeypatch_axis_labels
monkeypatch_axis_labels()

# Import own utility functions
import niceplot.utils as utils

# Create custom colormap
N = plt.cm.plasma.N
cmaplist_magma = [plt.cm.magma(i) for i in range(N)]

cmaplist = [plt.cm.plasma(i) for i in range(N)]
cmaplist[0] = mpl.colors.to_rgba('black')
cmaplist[-1] = cmaplist_magma[-1]

mycmap = mpl.colors.LinearSegmentedColormap.from_list('Custom cmap', cmaplist, N)
mycmap.set_bad('gainsboro')

def draw2dplot(
    x: pd.core.series.Series,
    y: pd.core.series.Series,
    binrange: list,
    nbins: int,
    xlab: str = None,
    ylab: str = None,
    z: pd.core.series.Series = None,
    zopt: str = "counts",
    suffix: str = "",
    addinfo: str = "",
    output_dir: str = None,
    addnumbers: bool = False,
    doballs: bool = False
  ) -> None:
  """Function to draw a 2D histogram of x vs y."""
  # Replace x- and y-axis labels by nice strings if custom xlab and ylab are not provided:
  xlab = utils.getnicestr(x.name) if xlab == None else xlab
  ylab = utils.getnicestr(y.name) if ylab == None else ylab
  fig, ax = plt.subplots(nrows=1, ncols=1)
  
  # Get automatic range and nbins if values are not provided:
  binrange = binrange if binrange != None else [ [min(x.values), max(x.values)], [min(y.values), max(y.values)]]
  nbins = nbins if nbins != None else 50
  #TODO: fix log-log plot using this binning sheme:
  # nbins = [np.logspace(-4, 0, nbins), np.logspace(-4, 0, nbins)]
  
  # Make 2d hist (defending on zopt):
  if zopt == "counts":
    z_matrix, x_edges, y_edges, h = ax.hist2d(x, y, bins=nbins, range=binrange, cmin=1)
    clab = 'no. of models'
    figname = f'2dhist_{x.name}_vs_{y.name}_{suffix}.pdf'
    anncol = 'white'
    numdig = 0

  else:
    # Plot fraction of excluded models on z-axis. First, cast data into dataframe:
    df = pd.DataFrame( {
      'x': x,
      'y': y,
      'z': z
    } )
    
    # Next, we make a simple histogram to get the bin edges:
    counts, x_edges, y_edges = np.histogram2d(x, y, bins=nbins, range=binrange)
    
    # Bugfix for including 0. values:
    x_edges[0] = x_edges[0]-1e-9 if x_edges[0] == 0. else x_edges[0]
    y_edges[0] = y_edges[0]-1e-9 if y_edges[0] == 0. else y_edges[0]
        
    # Apply bins to df:
    # Bin the data for 'x' and 'y' columns
    bins_x = pd.cut(df['x'], bins=x_edges)
    bins_y = pd.cut(df['y'], bins=y_edges)

    if zopt == "excl_frac":
      z_excl = df.groupby([bins_x, bins_y], observed=False)['z'].apply(utils.frac_excl)
      clab = "Fraction of Excluded Models"
    elif zopt == "excl_max":
      z_excl = df.groupby([bins_x, bins_y], observed=False)['z'].apply(np.maximum.reduce)
      clab = "Maximum CLs value"
    else:
      raise ValueError(f"Value {zopt} for zopt is not supported!")

    # Reshape the data for plotting
    z_matrix = z_excl.unstack().values

    # Create a 2D color plot
    if not doballs:
      h = ax.pcolormesh(x_edges, y_edges, z_matrix.T, cmap=mycmap, vmin=0, vmax=1)
      figname = f'2dexcl_{zopt}_{z.name}_{x.name}_vs_{y.name}_{suffix}.pdf'
    else:
      # Calculate bin centers
      x_centers = (x_edges[:-1] + x_edges[1:]) / 2
      y_centers = (y_edges[:-1] + y_edges[1:]) / 2
      
      # grey background:
      h = ax.pcolormesh(x_edges, y_edges, z_matrix.T*np.nan, cmap=mycmap, vmin=0, vmax=1)
      # add balls:
      h = ax.scatter(x_centers.repeat(nbins), np.tile(y_centers, nbins), s=counts**2+3, c=z_matrix, cmap=mycmap, vmin=0, vmax=1)
      figname = f'2dexcl_balls_{zopt}_{z.name}_{x.name}_vs_{y.name}_{suffix}.pdf'
  
    addinfo += f", {z.name}"
    anncol = 'black'
    numdig = 2

  # Plot dashed grey line if mN1 on y axis:  
  if "m_chi_10" in y.name:
    xylinearr = np.linspace(min(ax.get_ylim()[0], ax.get_xlim()[0]), max(ax.get_ylim()[1], ax.get_xlim()[1]), 1000)
    ax.plot(xylinearr, xylinearr, linestyle='dashed', color='grey')

  # Overlay simplified model limits if they exist:
  simplified_limit = utils.get_simplified_limit(x.name, y.name, z)
  if simplified_limit is not None:
    ax.plot(simplified_limit[x.name], simplified_limit[y.name], linestyle='-', color='white', linewidth = 2.0)
    ax.plot(simplified_limit[x.name], simplified_limit[y.name], linestyle='--', color='black')
    

  if addnumbers:
    # Annotate numbers:  
    x_width = x_edges[1] - x_edges[0]
    y_width = y_edges[1] - y_edges[0]
    for i in range(len(x_edges) -1):
      for j in range(len(y_edges) -1):
        if f'{z_matrix[i, j]:.2f}' == 'nan': continue
        ax.annotate(f'{z_matrix[i, j]:.{numdig}f}', (x_edges[i] + x_width/2., y_edges[j] + y_width/2.), color=anncol, ha='center', va='center', fontsize=7)

  # Fix labels, offsets and layout:
  cbar = fig.colorbar(h, ax=ax)
  cbar.set_label(clab, fontsize=13)
  ax.set_xlabel(xlab, fontsize=13)
  ax.set_ylabel(ylab, fontsize=13)
  #TODO: fix log-log scale to work properly
  # ax.set_yscale('log')
  # ax.set_xscale('log')
  
  # Correct offset for potential exponential on x and y axes; fix layout:
  ax.xaxis._update_offset_text_position = types.MethodType(utils.bottom_offset, ax.xaxis)
  ax.yaxis._update_offset_text_position = types.MethodType(utils.top_offset, ax.yaxis)
  fig.tight_layout(rect=(0, 0, 1, 0.94)) # default: left=0, bottom=0, right=1, top=1
  
  # Add ATLAS label + info:
  if addinfo == "":
    atlasify("Internal", outside=True) 
  else:
    atlasify("Internal", addinfo, outside=True) 
  
  # Save:
  return utils.savefile(fig, output_dir, figname)