import os
import pandas as pd
import numpy as np
from scipy.stats import zscore
import statsmodels.api as sm
from .generate_plots import *
lowess = sm.nonparametric.lowess


## Function summary --------------------------------------------------------

# ModelCracking() takes a dataframe of the surface profile and extracts
# descriptive information about the cracks

## original_data = a data frame containing the x and z measurements from a single 
## line measurement
## file = the .txt file currently being analyzed
## which_line = a number to identify each line measurement if using batch_cracking
## first_surf = first percentile of data where cracks can be looked for
## last_surf = last percentile of data where cracks can be looked for
## span = parameter for loess() outlier detection algorithm (controlls amount of smoothing of the model)
## plot_stats = should the density plots for width and depth be saved to the 
## output folder
## plot_visual = should the visual confirmation summary be saved to the output 
## folder (HIGHLY recommended)
## Returns a pandas dataframe containing the final crack analysis.
def g_model_cracking(output_directory: str, original_data: object, file: str, which_line: int=-1, first_surf: float=0.0, last_surf: float=1.0, span: float = 0.05, plot_stats: bool=True, plot_visual: bool=True):
    """Analyzes and plots cracks, and returns a Pandas Dataframe containing analyzed cracks

   :param output_directory: Directory where plots will be generated.
   :type output_directory: str
   :param original_data: The Dataframe with columns (x, y, z) containing the linescan data.
   :type original_data: Pandas Dataframe
   :param file: The name of the .txt file containing the data to be analyzed (used to format output file names)
   :type file: str
   :param which_line: A number to identify each line measurement if using batch_cracking
   :type which_line: int
   :param first_surf: Start of proportion of data where cracks can be looked for (between 0 and 1)
   :type first_surf: float
   :param last_surf: End of proportion of data where cracks can be looked for (between 0 and 1)
   :type last_surf: float
   :param span: Parameter for loess() outlier detection algorithm between 0 and 1(controlls amount of smoothing of the model)
   :type span: float
   :param plot_stats: Whether or not the density plots for width and depth should be saved to the output folder
   :type plot_stats: boolean
   :param plot_visual: Whether or not the visual confirmation summary should be saved to the output folder (HIGHLY recommended)
   :type plot_visual: boolean
   :return: A Pandas Dataframe containing the final crack analysis.
   :rtype: Pandas Dataframe with columns (start, end, id, mid.x, mid.z, mid.z.base, depth, width, min.z, points)
    """
    
    ###create output directories and output file names

    file_parts = os.path.splitext(file)
    name = file_parts[0]

    if which_line == -1:
        file_no_txt = f"{file_parts[0]}"
    else:
        file_no_txt = f"{file_parts[0]}-{which_line}"

    if not os.path.exists(os.path.join(output_directory, "output")): 
        os.makedirs(os.path.join(output_directory, "output"))

    if not os.path.exists(os.path.join(output_directory, "output", name)): 
        os.makedirs(os.path.join(output_directory, "output", name))
    

    file_visual = os.path.join(output_directory, "output", name, "visual", f"{file_no_txt}-visual.png")
    file_depth = os.path.join(output_directory, "output", name, "depth", f"{file_no_txt}-depth.png")
    file_width = os.path.join(output_directory, "output", name, "width", f"{file_no_txt}-width.png")
    file_baseline = os.path.join(output_directory, "output", name, "baseline", f"{file_no_txt}-baseline.png")


    ###Load data
    original_data = original_data[['x', 'z']]

    # make sure there is no invalid data points (invalid points have z = -1)
    remove = original_data['z'] == -1 
    original_data = original_data[~remove]
    # reset to keep index accurate
    original_data.reset_index(inplace = True, drop = True)

    print("Identifying outliers...")
    
    # used to speed up lowess calculation
    delta = (original_data['x'].max() - original_data['x'].min()) * 0.01 

    print("Fitting spline...")
    x_fit, z_fit = lowess(original_data['z'], original_data['x'], delta = delta, frac = span, return_sorted= True).T

    #store prediction of each point, residual, z_score of residual, and if its an outlier
    
    original_data['pred'] = z_fit
    original_data['resid'] = original_data['z'] - original_data['pred']
    original_data["z_scores"] = zscore(original_data['resid'])
    #outliers are when residuals are <-2 z scores away
    original_data["outlier"] = original_data["z_scores"] < -2 
    

    print("Analyzing cracks...")

    # Note: points outside first.surf:last.surf are excluded because that's where the metal test jig causes the backsheet to
    # bend downwards a lot.  Often this will be falsely identified as a crack if it's not removed first.
    # first_surf and last_surf should be specific to each sample

    #convert first/last surf percentage to values
    first_surf = round(first_surf*(len(original_data.index) - 1))
    last_surf = round(last_surf*len(original_data.index) - 1)

    #create dataframe to store crack analysis data
    crack_analysis = pd.DataFrame([], columns=['start', 'end'])
    index = first_surf

    #Find individual cracks from original data
    # Cracks are spans of points that are outliers or are separated by less than 10 non-outliers
    while index < last_surf:
        # Skip line if it is not an outlier
        if original_data.loc[index]["outlier"] == False:
            index += 1
            continue
        
        # If an outlier is detected, begin the crack
        start = index
        end = index
        gap = 0

        ## Count any up-down spikes within 10 microns of another crack into a single crack
        while gap < 10 and index < last_surf :
            # while in the crack
            index += 1
            if original_data.loc[index]["outlier"] == False:
                gap += 1
            else:
                gap = 0
                end = index
        #add the crack to crack_analysis
        crack_analysis.loc[len(crack_analysis.index)] = [start, end]

    # remove any "cracks" that are less than 3 microns wide
    remove = crack_analysis['end'] - crack_analysis['start'] < 3
    crack_analysis = crack_analysis[~remove]
    crack_analysis.reset_index(inplace = True, drop = True)

    # setup columns for crack_analysis
    crack_analysis['id'] = file_no_txt
    crack_analysis['mid.x'] = np.nan
    crack_analysis['mid.z'] = np.nan
    crack_analysis['mid.z.base'] = np.nan
    crack_analysis['depth'] = np.nan
    crack_analysis['width'] = np.nan
    ##stats calculations
    if len(crack_analysis.index) > 0:
        for i in range(len(crack_analysis)):
            crack_points = original_data.iloc[crack_analysis.at[i, 'start']:crack_analysis.at[i, 'end']]
            crack_points.reset_index(inplace = True, drop = True)
            crack_analysis.at[i, 'width'] = crack_points.at[len(crack_points.index)-1, 'x'] - crack_points.at[0, 'x']
            crack_analysis.at[i, 'mid.x'] = crack_points.at[len(crack_points.index)//2, 'x']
            crack_analysis.at[i, 'mid.z'] = crack_points.at[len(crack_points.index)//2, 'z']
            crack_analysis.at[i, 'mid.z.base'] = crack_points.at[len(crack_points.index)//2, 'resid']
            crack_analysis.at[i, 'min.z'] = np.min(crack_points['z'])
            crack_analysis.at[i, 'depth'] = np.mean(np.min(crack_points['z']) - crack_points['pred'])

        crack_analysis['width'] = round(crack_analysis['width']*1000) # Convert from mm to microns
        crack_analysis['points'] = len(original_data) #points in linescan
    
    stats_output_directory = os.path.join(output_directory, "output", name, "stats")
    if not os.path.exists(stats_output_directory):
        os.makedirs(stats_output_directory)

    #saves a csv of the stats
    final_analysis = crack_analysis.copy()
    final_analysis.to_csv(os.path.join(stats_output_directory, f"{file_no_txt}-CrackData.csv"), index=False)


    #creates a plot of the data + plot of the baselined data (to the spline)
    if plot_visual:
        print("Plotting and saving output...")

        visual_output_directory = os.path.join(output_directory, "output", name, "visual") #create directories
        if not os.path.exists(visual_output_directory):
            os.makedirs(visual_output_directory)

        visual_output_directory = os.path.join(output_directory, "output", name, "baseline")
        if not os.path.exists(visual_output_directory):
            os.makedirs(visual_output_directory)

        create_visualization_plot(original_data, original_data, crack_analysis, file_visual, 0.25, file_no_txt)
        create_baseline_plot(original_data, original_data, crack_analysis, file_baseline, file_no_txt)
    
    #creates plots of the width and depth of the cracks
    if plot_stats:
        stats_output_directory = os.path.join(output_directory, "output", name, "depth")
        if not os.path.exists(stats_output_directory):
            os.makedirs(stats_output_directory)

        stats_output_directory = os.path.join(output_directory, "output", name, "width")
        if not os.path.exists(stats_output_directory):
            os.makedirs(stats_output_directory)

        create_depth_plot(crack_analysis['depth']*-1, file_depth, f"Depth Distribution ({file_no_txt})")
        create_width_plot(crack_analysis['width'], file_width, f"Width Distribution ({file_no_txt})")

    return final_analysis
