import click
from tqdm import tqdm

# Own imports:
from niceplot.draw2d import draw2dplot
from niceplot.draw1d import draw1dratio
import niceplot.utils as utils
from niceplot.reader import Reader

@click.command()
@click.argument('config_file')
def niceplot(config_file: str) -> None:
    """Module to make nice looking root plots in the ATLAS Style.
    See https://gitlab.cern.ch/jwuerzin/nice-plot or https://pypi.org/project/niceplotpy/ for documentation.
    """
    # Print welcome message and version number:
    utils.printwelcome()
    
    # Read in config file and prep corresponding dictionary with pandas.DataFrames:
    reader = Reader(config_file)   
    utils.paddefaults(reader, mode='reader')
    
    dfdict = reader.prepdfdict()

    savestr = "\n"

    # Loop over all configurations and plotting configs; Make one plot for all configs & plot configs:
    # for plot in reader.plots:
    for plot in tqdm(reader.plots, desc="Generating Plots", unit="plots"):
        utils.paddefaults(plot, mode='plot')
        
        if plot.type == '2dhist':
            # Make one 2D (exclusion) Histogram for every dataframe configuration:
            for config in reader.configurations:
                savestr += draw2dplot(
                    x=dfdict[config.name].get(plot.x),
                    y=dfdict[config.name].get(plot.y),
                    binrange=plot.range,
                    nbins=plot.nbins,
                    z=dfdict[config.name].get(plot.z),
                    zopt=plot.zopt,
                    suffix=config.name,
                    addinfo=config.addinfo,
                    output_dir=f"{reader.output_dir}/{plot.subdir}",
                    addnumbers=plot.addnumbers,
                    doballs=plot.doballs
                )
        elif plot.type == '1dratio':
            # Make one 1dratio plot with specific configuration:
            savestr += draw1dratio(
                dfdict=dfdict,
                denominator=plot.denominator,
                numerator=plot.numerator,
                x=plot.x,
                range=plot.range,
                ylab=plot.ylab,
                denomlab=utils.getaddinfo(reader.configurations, plot.denominator),
                numlab=utils.getaddinfo(reader.configurations, plot.numerator),
                nbins=plot.nbins,
                suffix=f"{plot.denominator}_over_{plot.numerator}",
                logy=plot.logy,
                output_dir=f"{reader.output_dir}/{plot.subdir}"
            )
        else:
            raise(ValueError(f"Plot type {plot.type} not recognised! Supported types are: 2dhist and 1dratio"))
        
    print(savestr)
    print("Plots generated successfully. Have a great day!!")