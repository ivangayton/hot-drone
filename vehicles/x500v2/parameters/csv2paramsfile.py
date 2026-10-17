#!/usr/bin/env python3

import sys, os
import csv
import argparse
import pathlib

def overwrite(inp, outp):
    """
    Create a new list of text lines for a QgroundControl .params file
    
    Parameters
    --------
    inp : list
        A list of lists, each sublist has two elements, key and value
    outp : list
        A list of strings, the first character of the first few items is
        a hash indicating it's commented out. Other lines are of form:
        Vehicle-Id\tComponent-ID\tName\tValue\tType

    Returns:
    -------
    A list of strings that can be written as lines to a new .params file
    """
    ind = dict(inp)
    newlines = []
    for line in outp:
        outline = line
        cols = line.split('\t')
        if len(cols) == 5:
            param = cols[2]
            outval = cols[3]
            newval = None
            if param in ind:
                newval = ind[param]
            if newval:
                outvalnum = outval
                if int(cols[4]) >= 9:
                    outvalnum = round(float(outval),7)
                elif int(cols[4]) < 9:
                    outvalnum = int(outval)
                if float(newval) != float(outval):
                    outval = newval
                    outline = (f'{cols[0]}\t{cols[1]}\t'
                               f'{param}\t{newval}\t'
                               f'{int(cols[4])}\n')
        newlines.append(outline)
    return newlines
   
        

if __name__ == "__main__":
    """
    Create a new .params file by copying the structure of a properly formatted
    QGroundControl .params file, overwriting any different parameter values
    found in a CSV with only 2 columns, MAVLink parameter and value,
    """
    p = argparse.ArgumentParser(usage="usage: attachments [options]")
    p.add_argument('csvfile', help = "Text CSV file with params and values")
    p.add_argument('paramsfile', help = "QGroundControl-style params file")
    args = p.parse_args()
    
    inparams = list(csv.reader(open(args.csvfile)))
    outparams = list(open(args.paramsfile).readlines())

    newparams = overwrite(inparams, outparams)

    outpath = os.path.splitext(args.paramsfile)[0]
    outfilename = f'{outpath}_merged.params'
    outfile = open(outfilename, 'w')
    outfile.writelines(newparams)

    
    
