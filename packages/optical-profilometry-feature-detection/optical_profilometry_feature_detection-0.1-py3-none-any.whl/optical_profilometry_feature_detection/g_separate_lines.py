import os
import pandas as pd

def g_separate_lines(input_directory: str, file: str):
    """Converts a raw .txt data file into individual dataframes of linescans.

    :param input_directory: Directory where the .txt file containing the data to be converted is.
    :type input_directory: str
    :param file: The name of the .txt file containing the data to converted.
    :type file: str
    :return: A list of Pandas Dataframes containing the individual separated line scans. Columns are (x, y, z).
    :rtype: list[Pandas Dataframe]
    """
    combined = pd.read_csv(os.path.join(input_directory, file), header=None, names=["x", "y", "z"])
    
    consecutive = combined[combined["z"]!=-1] #remove bad readings
    separated_lines = []
    row = 1
    while row < len(consecutive):
        start_line = row - 1
        while row < len(consecutive.index) and (consecutive["y"].iloc[row] - consecutive["y"].iloc[row-1] < 0.05): #if the data points are close enough together
            row+=1
        separated_lines.append(consecutive.iloc[start_line:row]) #if they arent close enough, start a new line 
        row+=1
    return separated_lines
