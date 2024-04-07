#!/bin/python3
from os import system
from sys import argv

BIN_DIR = "bin"
RES_DIR = "res"
CASE_NAMES = {
    'bt',
    'cg',
    'ep',
    'ft',
    'is',
    'lu',
    'mg',
    'sp'
}
SCALE_NAMES = {
    # 'S',
    # 'W',
    'A',
    'B',
    'C'
}

THREADS_COUNTS = [
    112, 
    56, 
    28, 
    16, 
    8, 
    4, 
    2
]

def doesFileExist(file_path):
    try:
        with open(file_path):
            return True
    except FileNotFoundError:
        return False    

def checkCase(case_n):
    if case_n not in CASE_NAMES:
        print(f"unknown provided case: {case_n}")
        exit(1)

def checkScale(scale_n):
    if scale_n not in SCALE_NAMES:
        print(f"unknown provided scale: {scale_n}")
        exit(1)

def getFilePath(case_n, scale_n, num_threads):
    """Get the file path for the result file"""
    file_name = f"{case_n}.{scale_n}.t{num_threads}"
    file_path = f"./{RES_DIR}/{file_name}"
    return file_path

def wasTestRun(case_n, scale_n, num_threads):
    """Check if a test was run by checking if the result file exists"""
    file_path = getFilePath(case_n, scale_n, num_threads)
    return doesFileExist(file_path)

def getRunCmd(case_n, scale_n, num_threads):
    base_name = f"{case_n}.{scale_n}"
    return f"OMP_NUM_THREADS={num_threads} ./{BIN_DIR}/{base_name} > { getFilePath(case_n, scale_n, num_threads)}"

def runSample(case_n, scale_n, num_threads=224):
    """Run a sample and print the output"""
    checkCase(case_n)
    checkScale(scale_n)
    output_path = getFilePath(case_n, scale_n, num_threads)
    if not wasTestRun(case_n, scale_n, num_threads):
        system(getRunCmd(case_n, scale_n, num_threads))
        system(f"cat {output_path}")
    else:
        print(f"skipping '{output_path}' (already run)")

def runMake(*args):
    system(f"make {' '.join(args)}")

def mainBuildAll(args):
    for case_n in CASE_NAMES:
        for scale_n in SCALE_NAMES:
            runMake(case_n, f"CLASS={scale_n}")

def mainRunOneSample(args):
    case_n = 'cg'
    scale_n = 'B'

    if len(argv) >= 3:
        case_n = args[1]
        scale_n = args[2]

    runSample(case_n, scale_n)

def iterCoreVar(case_n, scale_n):
    for num_cores in THREADS_COUNTS:
        runSample(case_n, scale_n, num_cores)

def iterScaleVar(case_n):
    for scale_n in ['A', 'B', 'C']:
        iterCoreVar(case_n, scale_n)

def iterCaseVar():
    for case_n in CASE_NAMES:
        iterScaleVar(case_n)

if __name__ == "__main__":
    if len(argv) >= 2 and argv[1] == 'build':
        build_all(argv)
    else:
        iterCaseVar()