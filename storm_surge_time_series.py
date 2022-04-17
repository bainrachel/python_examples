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

filedata = read_file_lines('NOAA_8728690_data.txt')
filedata = filedata[11:] #get rid of the first 10 lines, which are header lines
out_dict = split_file_columns(filedata)
timestamp = out_dict['column_0']
timestamp = reformat_string_date(timestamp)
z_predicted = out_dict['column_1']
z_predicted_number = [float(val) for val in z_predicted]
z_measured = out_dict['column_2']
z_measured_number = [float(val) for val in z_measured]

fig1 = plt.figure(figsize=(10,4))
plt.plot(timestamp, z_predicted_number, label='Predicted')
plt.plot(timestamp, z_measured_number, label='Measured')
plt.legend()
plt.ylabel('Water level (m, NAVD88)')
plt.title('Water level at Apalachicola, FL, before and after Hurricane Michael')
plt.show()