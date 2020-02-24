#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""
NAME  : ashclouds.py
AUTHOR: Alexandre Fukaya
DATE  : 23/02/2020

DESCRIPTION:
    Resolução do problema para o espalhamento de nuvens de cizas vulcânicas 
    proposto em https://www.dcc.fc.up.pt/oni/problemas/2010/qualificacao/probB.html
    
DEPENDENCIES:

TODO:
    
"""
import sys
import os
import copy

def load_data(file_path, file_name):
    data      = list()
    data_file = file_path + file_name

    with open(data_file) as f:
        for line in f:
            data.append(line)
    return data

def transform_data(data):
    size_info = data[0].strip('\n').split(' ')
    lin = int(size_info[0])
    col = int(size_info[1])
    data_array = []
    airports = 0

    for i in range(1,lin+1):
        data_line = data[i].upper().strip('\n')
        airports = airports + data[i].count('A')
        data_array.append(list(data_line))
    return airports, lin, col, data_array

def simulate_clouds(airports, max_lines, max_cols, data):
    airports_affected = 0
    day               = 0
    end_simulation    = False
    max_data          = 0
    min_data          = 0

    today_data = copy.deepcopy(data)

    print('Vulcanic Ash Clouds Simulator')
    print()

    while(not end_simulation):
        # For each pass clone the matix and make the changes at the copy.
        # Store the copy for output and calculations.
        tomorrow_data = copy.deepcopy(today_data)
        lin = 0

        # Print the status for current the day
        print('Day {0}'.format(day))
        print('Airports affected {0}'.format(airports_affected))
        print('Current Status')
        for line in today_data: print(line)
        print()

        # Calculates the next day status.
        for data_line in today_data:
            col = 0
            for info in data_line:
                if info == '#': # found a ash cloud, need to check boundaries
                    neg_col = col - 1
                    neg_lin = lin - 1
                    pos_col = col + 1
                    pos_lin = lin + 1

                    # Check coordinates for out of boudaries values.
                    if neg_col < 0 : neg_col = 0
                    if neg_lin < 0 : neg_lin = 0
                    if pos_col > max_cols  - 1 : pos_col = max_cols  - 1
                    if pos_lin > max_lines - 1 : pos_lin = max_lines - 1

                    # Cover neighborhoods with ashes
                    tomorrow_data[lin][neg_col] = '#'
                    tomorrow_data[lin][pos_col] = '#'
                    tomorrow_data[neg_lin][col] = '#'
                    tomorrow_data[pos_lin][col] = '#'

                col = col + 1
            lin = lin + 1

        # Check for affected airports
        for today_line,tomorrow_line in zip(today_data,tomorrow_data):
            for today_value,tomorrow_value in zip(today_line,tomorrow_line):
                if (today_value == 'A') and (today_value != tomorrow_value):
                    if (airports_affected == 0) : min_data = day + 1

                    airports_affected += 1

                    if (airports_affected == airports) : 
                        max_data = day + 1 
                        end_simulation = True

        today_data = tomorrow_data
        day = day + 1

    # Print last day status
    print('Day {0}'.format(day))
    print('Airports affected {0}'.format(airports_affected))
    print('Current Status')
    for line in today_data: print(line)
    print()

    # Print simmulation summary
    print('Simularion ended')
    print('Days before the first airport is reached {0}'.format(min_data))
    print('Days before all airports are affected {0}'.format(max_data))
    return 

def main():
    file_path = '.\\'
    file_name = 'ash1.txt'
    raw_data = load_data(file_path,file_name)
    airport_count, max_lines, max_cols, ash_data = transform_data(raw_data)
    simulate_clouds(airport_count, max_lines, max_cols, ash_data)

if __name__ == "__main__":
    main()