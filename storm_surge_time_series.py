"""
Script for reading, cleaning, and plotting water level data stored in a text file.

The data in this example are publicly-available water level measurements from the
National Oceanographic and Atmospheric Administration (NOAA). However, the original
NOAA data have been reformatted, and several errors have been added to the raw
data file for teaching purposes.

This script was written in Python 3.9.7.
"""

import datetime as dt
import matplotlib.pyplot as plt

def read_file_lines(filename):
    """
    Reads all lines in a file and stores in a list
    """
    in_file = open(filename, 'r') #Open the file
    lines = in_file.readlines() #Read the individual lines of the file
    in_file.close() #Close the file
    return lines

def find_bad_lines(textlist_in):
    """
    Function checks whether each line of textlist_in contains 2 whitespace characters.
    It returns a list of indices of the lines that contain fewer than 2 whitespace characters.
    (This is a very specific example for this teaching exercise. A more general function
    could be substituted for real-world application.)
    """
    bad_line_inds = [] #create an empty list to hold the indices of the bad lines
    line_counter = 0 #keep track of which line we're on
    for this_line in textlist_in: #for each line of the input text...
        num_whitespace = this_line.count(' ') #count the number of whitespace characters
        if num_whitespace != 2:
            bad_line_inds.append(line_counter) #add the index of the bad line to the output list
        line_counter += 1
    return bad_line_inds

def split_file_columns(data_in):
    """
    Takes the contents of a text file and splits it at every whitespace
    to produce columns of data. It automatically determines the number of
    columns based on the formatting of the first line of the text file. If
    the text file has a header naming the data columns, set has_header to 1;
    otherwise automatic column names will be generated.
    """
    #Using the first line, determine the number of columns and set up output structure.
    line1 = data_in[0]
    line1_split = line1.split(' ') #split at whitespace
    n_col = len(line1_split)
    out_dict = {} #empty dictionary to hold the output
    for i in range(len(line1_split)):
        this_key = 'column_' + str(i) #create a unique dictionary key
        out_dict[this_key] = [] #empty list within the dictionary to hold the output

    #Now loop through all lines of the input data, split into columns, and store
    #in dictionary.
    for this_line in data_in:
        line_temp = this_line.replace('\n','') #remove the newline character from the end of the string
        line_temp = line_temp.split(' ') #split at whitespace
        for i in range(len(line_temp)):
            if i <= n_col: # allow for the possibility that a given line may erroneously have extra whitespace, and only use columns matching the size of the output dictionary
                this_key = 'column_' + str(i)
                out_dict[this_key].append(line_temp[i]) #add value to lists in dictionary
    return out_dict

def reformat_string_date(string_date_in):
    """
    Convert strings in the form YYYYMMDDhhmm into datetime values.
    """
    date_out = [] #empty list to hold the output
    for val in string_date_in:
        year_temp = int(val[0:4]) #convert year to integer
        month_temp = int(val[4:6]) #convert month to integer
        day_temp = int(val[6:8]) #convert day to integer
        hour_temp = int(val[8:10]) #convert hour to integer
        minute_temp = int(val[10:]) #convert minute to integer
        date_out.append(dt.datetime(year_temp, month_temp, day_temp,
                                    hour_temp, minute_temp, 0)) #convert to datetime
    return date_out

def make_time_series_plot(x_vals, y_vals, x_label=None, y_label=None, titlestring=None, labels=None):
    """
    This function makes a time series plot with one or more lines.

    x_vals: list of values to plot on the horizontal axis
    y_vals: list of values to plot on the vertical axis. If you want to plot multiple lines
        in the same figure, y_vals can also be a list of lists, with each interior list
        containing the y-values for one of the lines.
    xlabel: string containing the label for the horizontal axis
    ylabel: string containing the label for the vertical axis
    title: string containing the plot title
    labels: list of strings containing the legend contents. labels should have the same length
        as y_vals
    """
    fig1 = plt.figure(figsize=(8, 3)) #create an empty figure

    #If labels was empty or had the wrong length, create some dummy labels
    if (labels is None) or (len(labels) != len(y_vals)):
        labels = [] #empty list to hold the line labels
        for i in range(len(y_vals)): #for each list in y_vals, create a new label
            labels.append('Line_' + str(i))

    #This is the part that does the plotting
    if len(x_vals) == len(y_vals): #If x_vals and y_vals have the same length, create a figure with a single line.
        plt.plot(x_vals, y_vals, label=labels[0])
    elif type(y_vals[0]) != list: #if y_vals is still a list of numbers but just has the wrong length, return an error message
        print('y_vals is not the same length as x_vals.')
    else: #Check if y_vals is a list of lists, with each list containing y-data for one line
        counter = 0 #keeps track of which element of y_vals we're currently working on
        for this_y in y_vals: #for each list within y_vals
            if len(x_vals) == len(this_y):
                plt.plot(x_vals, this_y, label=labels[counter])
            else: #output an error message
                print('Element ' + str(counter) + ' of y_vals is not the same length as x_vals.')
            counter =+ 1 #increment the counter by 1

    #Now add the labels and the title
    plt.legend()
    if x_label is not None:
        plt.xlabel(x_label)
    if y_label is not None:
        plt.ylabel(y_label)
    if titlestring is not None:
        plt.title(titlestring)
    return fig1

def pop_multiple(list_in, inds_to_delete):
    """
    This is a function which deletes multiple elements from a list... basically
    the equivalent of using "pop" multiple times for removing individual elements.

    list_in: original list
    inds_to_delete: indices of the elements of list that should be deleted
    """
    new_list = [val for ind, val in enumerate(list_in) if ind not in inds_to_delete]
    return new_list

#Read the text file
filedata = read_file_lines('NOAA_8728690_data.txt')

#Delete the first 10 lines of the file (these are header lines)
filedata = filedata[11:] #get rid of the first 10 lines, which are header lines

#Find the indices of the bad lines.
#(For this simple example, the "good" lines contain exactly two whitespace characters.
#Any line which contains fewer or more than two whitespace characters is considered "bad".)
bad_line_inds = find_bad_lines(filedata)

#Delete the bad lines from the file
filedata_new = pop_multiple(filedata, bad_line_inds)

#Split the text file at the whitespace characters to produce three columns of data
out_dict = split_file_columns(filedata_new)

#The timestamps are the first entry in the dictionary. Let's pull those
#out and clean them up into a plottable format.
timestamp = out_dict['column_0'] #get data from dictionary
timestamp = reformat_string_date(timestamp) #Reformat the date from YYYYMMDDhhmm into a Python datetime

#The water level predictions are the second entry in the dictionary, and the
#water level measurements are the third entry in the dictionary. We'll pull
#those out and convert them from strings into floats so we can plot the values.
z_predicted = out_dict['column_1']
z_predicted_number = [float(val) for val in z_predicted] #convert string to float
z_measured = out_dict['column_2']
z_measured_number = [float(val) for val in z_measured] #convert string to float

#Now we can plot the data!
my_figure = make_time_series_plot(timestamp,
                                  [z_predicted_number, z_measured_number],
                                  x_label=None,
                                  y_label='Water level (m, NAVD88)',
                                  titlestring='Water level at Apalachicola, FL, before and after Hurricane Michael',
                                  labels=['Predicted', 'Measured'])
plt.show()