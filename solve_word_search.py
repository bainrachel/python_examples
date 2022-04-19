"""
Script solves a word search with the words oriented across or down.
(No words are backwards, and no words are on the diagonal.)

The output indicates the row and column for the first letter of
each word, along with indicating whether the word is horizontal
or vertical.

This script was written in Python 3.9.7.
"""

def read_file_lines(filename):
    """
    Reads all lines in a file and stores in a list
    """
    in_file = open(filename, 'r') #Open the file
    lines = in_file.readlines() #Read the individual lines of the file
    in_file.close() #Close the file
    return lines

def transpose_lists(lists_in):
    """
    Transposes a list of lists. The input data should be in the form [[a1, a2, ... aN],
    [b1, b2, ... bN], ... [x1, x2, ... xN]]. The output data will have the form
    [[a1, b1, ... x1],[a2, b2, ... x2],...,[aN, bN,... xN]].
    """
    transposed_lists = [[lists_in[j][i] for j in range(len(lists_in))] for i in range(len(lists_in[0]))]
    return transposed_lists

def find_word(word, search_strings):
    """
    Searches for a word in a list of strings.
    The output is the index (indices) in search_strings which contain the word,
    and the index within that string where the first letter of the word occurs.
    IMPORTANT: THIS IS CASE-SENSITIVE.
    """
    word_location_out = [] #this will hold the output
    string_counter = 0
    for this_string in search_strings:
        num_occurrence = this_string.count(word)  # count the number of occurrences of the word. This is necessary because string.find() only returns the first occurrence.
        occurrence_counter = 0
        ind = 0 #initiate the search location at 0 (the beginning of the string)
        while occurrence_counter < num_occurrence: #find the first occurrence of the word, and then remove those letters and repeat until all occurrences are found.
            ind = this_string.find(word, ind) #search for word within this_string beginning at index ind
            word_location_out.append((string_counter, ind))
            occurrence_counter += 1 #increment so we move to the next occurrence
            ind +=1 #increment by 1 so the next search will ignore the occurrence(s) we already found
        string_counter += 1
    return word_location_out

def clean_text(text_in):
    """
    Function to remove tab and newline characters from a list of strings
    """
    clean_lines = []  # need to remove \t and \n
    for line in text_in:
        line_temp = line.replace('\n', '')  # remove the newline character from the end of the string
        line_temp = line_temp.replace('\t', '')  # remove the tabs
        clean_lines.append(line_temp)
    return clean_lines

#Read in the word search puzzle and clean
lines = read_file_lines('word_search.txt')
lines = clean_text(lines)

#Read in the list of words to search for
words = read_file_lines('word_search_list.txt')
words = clean_text(words)

solution_out = [] #this will hold the solution to the puzzle

#First, find all horizontal words
for word in words:
    locations_temp = find_word(word, lines)
    if len(locations_temp) > 0:
        for this_location in locations_temp:
            save_string = word + ', Row ' + str(this_location[0]) + ', Column ' + str(this_location[1]) + ', horizontal'
            solution_out.append(save_string)

#Now find all vertical words
lines_transpose = transpose_lists(lines) #transpose the puzzle so the vertical words are now horizontal
lines_transpose = [''.join(letters) for letters in lines_transpose] #concatenate individual letter strings into a single string
for word in words:
    locations_temp = find_word(word, lines_transpose)
    if len(locations_temp) > 0:
        for this_location in locations_temp:
            save_string = word + ', Row ' + str(this_location[1]) + ', Column ' + str(this_location[0]) + ', vertical'
            solution_out.append(save_string)

solution_alpha = sorted(solution_out) #alphabetize

with open('word_search_solution.txt', 'w') as f:
    f.write('\n'.join(solution_alpha))