#!/bin/python3

from a import *
from typing import Tuple
from json import dump
import subprocess

def runAndStringOut(cmd) -> str:
    """run the provided command, and redirect the stdout of it into the output string"""
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None


def extract_sample(case_n, scale_n, num_threads):
    """
    extract the runtime from the result file associated with the given sample.
    
    the format of the line in the result file which contains this information is:
        'Time in seconds = <float>'
    """
    sample_path = getFilePath(case_n, scale_n, num_threads)
    check_case(case_n)
    check_scale(scale_n)
    if not doesFileExist(sample_path):
        print(f"requested to extract sample with non-existant file: '{sample_path}'")
        return None
    
    line = runAndStringOut(f"cat {sample_path} | grep 'Time in seconds'")
    if line is None:
        return None
    timetok = [tok for tok in line.split(' ') if tok != ''][4]
    return float(timetok)

def main():
    all_res = dict()
    for case in CASE_NAMES:
        all_res[case] = dict()
        for scale in SCALE_NAMES:
            all_res[case][scale] = dict()
            for num_threads in THREADS_COUNTS:
                time = extract_sample(case, scale, num_threads)
                if time is not None:
                    all_res[case][scale][num_threads] = time
    with open('all_res.json', 'w') as resf:
        dump(all_res, resf, indent=4)

if __name__ == "__main__":
    main()