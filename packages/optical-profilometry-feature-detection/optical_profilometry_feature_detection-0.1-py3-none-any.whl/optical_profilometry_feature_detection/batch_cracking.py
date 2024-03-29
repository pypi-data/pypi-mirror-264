from .g_separate_lines import g_separate_lines
from .g_model_cracking import g_model_cracking

# batch_cracking works with files that contain multiple line scans, separated by different y values. 
# Each line scan must have their points be on the same y coordinate.
def batch_cracking(input_directory: str, output_directory: str, file: str, num_lines: int, first_surf: float=0.0, last_surf: float=1.0, span: float=0.05, plot_stats: bool=True, plot_visual: bool=True):
    """Analyzes multiple horizontal line scans in a single data file with different y coordinates for each scan

    :param input_directory: Directory where the txt file containing the data to be analyzed is.
    :type input_directory: str
    :param output_directory: Directory where plots will be generated.
    :type output_directory: str
    :param file: The name of the .txt file containing the data to be analyzed.
    :type file: str
    :param num_lines: The number of lines to be analyzed in the data file.
    :type num_lines: int
    :param first_surf: Start of proportion of data where cracks can be looked for (between 0 and 1)
    :type first_surf: float
    :param last_surf: End of proportion of data where cracks can be looked for (between 0 and 1)
    :type last_surf: float
    :param span: Parameter for loess() outlier detection algorithm between 0 and 1(controlls amount of smoothing of the model)
    :type span: float
    :param plot_stats: Whether or not the density plots for width and depth should be saved to the output folder.
    :type plot_stats: boolean
    :param plot_visual: Whether or not the visual confirmation summary should be saved to the output folder (HIGHLY recommended)
    :type plot_visual: boolean
    :return: None
    """
    list_of_lines = g_separate_lines(input_directory, file)

    if num_lines > len(list_of_lines):
        print("Requested number of lines is greater than number of line scans in the file.")
    
    #loops until either the specified number of lines or the number of lines in the file
    for x in range(1, min(num_lines+1, len(list_of_lines) + 1)):
        original_data = list_of_lines[x - 1]
        which_line = x

        g_model_cracking(output_directory, original_data, file, which_line, first_surf, last_surf, span, plot_stats, plot_visual)
    