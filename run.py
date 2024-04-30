#!/bin/python3
from os import system, geteuid
from sys import argv
from itertools import product
from tqdm import tqdm

BIN_DIR = "bin"
RES_DIR = "res"
VTUNE_DIR = "vtunes"
PERF_DIR = "perfs"
BYLINE_DIR = "byline"

CASE_NAMES = {
    'bt',
    # 'cg',
    # 'ep',
    # 'ft',
    # 'is',
    # 'lu',
    # 'mg',
    # 'sp'
}
SCALE_NAMES = {
    # 'S',
    # 'W',
    'A',
    'B',
    # 'C',
    # 'D'
}

THREADS_COUNTS = [
    # 224, 
    # 112, 
    56, 
    # 28, 
    # 16, 
    # 8, 
    # 4,
    # 2,
    # 1
]

def getAllSampleParams():
    return list(product(CASE_NAMES, SCALE_NAMES, THREADS_COUNTS))

def doesFileExist(file_path):
    try:
        with open(file_path):
            return True
    except FileNotFoundError:
        return False    
    except IsADirectoryError:
        return True

def checkCase(case_n):
    if case_n not in CASE_NAMES:
        print(f"unknown provided case: {case_n}")
        exit(1)

def checkScale(scale_n):
    if scale_n not in SCALE_NAMES:
        print(f"unknown provided scale: {scale_n}")
        exit(1)

def getResPath(case_n, scale_n, num_threads):
    """Get the file path for the result file"""
    file_name = f"{case_n}.{scale_n}.t{num_threads}"
    file_path = f"./{RES_DIR}/{file_name}"
    return file_path

def getVtuneDir(case_n, scale_n, num_threads):
    return f"./{VTUNE_DIR}/{case_n}.{scale_n}.{num_threads}"

def getExecPath(case_n, scale_n):
    return f"{BIN_DIR}/{case_n}.{scale_n}"

def wasTestRun(case_n, scale_n, num_threads):
    """Check if a test was run by checking if the result file exists"""
    file_path = getResPath(case_n, scale_n, num_threads)
    return doesFileExist(file_path)

def wasVtuneRun(cast_n, scale_n, num_threads):
    file_path = getVtuneDir(cast_n, scale_n, num_threads)
    return doesFileExist(file_path)

def runVtune(case_n, scale_n, num_threads, collection_type):
    outdir = getVtuneDir(case_n, scale_n, num_threads)
    if not wasVtuneRun(case_n, scale_n, num_threads):
        system(f"mkdir {outdir}")
        system(f"cd ./{outdir} && OMP_NUM_THREADS={num_threads} vtune -c {collection_type} ../../{getExecPath(case_n, scale_n)} -r {outdir}")
    else:
        print(f"skipping vtune run at '{outdir}' - already run")

def runSample(case_n, scale_n, num_threads=224):
    """Run a sample and print the output"""
    checkCase(case_n)
    checkScale(scale_n)
    output_path = getResPath(case_n, scale_n, num_threads)
    if not wasTestRun(case_n, scale_n, num_threads):
        system(f"OMP_NUM_THREADS={num_threads} ./{getExecPath(case_n, scale_n)} > {getResPath(case_n, scale_n, num_threads)}")
        system(f"cat {output_path}")
    else:
        print(f"skipping '{output_path}' (already run)")

def runMake(*args):
    system(f"make {' '.join(args)}")

def mainBuildAll(args):
    for case_n, scale_n in tqdm(list(product(CASE_NAMES, SCALE_NAMES))):
        runMake(case_n, f"CLASS={scale_n}")

def mainRunOneSample(args):
    case_n = 'cg'
    scale_n = 'B'

    if len(argv) >= 2:
        case_n = args[0]
        scale_n = args[1]
    runSample(case_n, scale_n)

def runAllSamples(args):
    for params in tqdm(getAllSampleParams()):
        runSample(*params)
        
def runAllVtuneHotspots(args):
    for params in tqdm(getAllSampleParams()):
        runVtune(*params, 'hotspots')

def getPerfOutputPath(case_n, scale_n, num_threads):
    return f"./{PERF_DIR}/{case_n}.{scale_n}.t{num_threads}.data"

def runPerf(case_n, scale_n, num_threads):
    data_path = getPerfOutputPath(case_n, scale_n, num_threads)
    exec_path = getExecPath(case_n, scale_n)
    system(f"numactl -N 0 perf record {exec_path} && mv perf.data {data_path}")

def ensureRoot():
    if geteuid() != 0:
        print("This script must be run as root.")
        exit(1)

def runAllPerf(args):
    ensureRoot()
    for params in tqdm(getAllSampleParams()):
        runPerf(*params)

def byline(case_n, scale_n, num_threads):
    data_path = getPerfOutputPath(case_n, scale_n, num_threads)
    byline_path = f"./{BYLINE_DIR}/{case_n}.{scale_n}.t{num_threads}.json"
    system(f"perf annotate -i {data_path} | ./annocol/main.py > {byline_path}")

def bylineAll(args):
    ensureRoot()
    for params in tqdm(getAllSampleParams()):
        byline(*params)
    
def mainCountSamples(args):
    items = {
        "Case": CASE_NAMES,
        "Scale": SCALE_NAMES,
        "Threadcount": THREADS_COUNTS,
    }
    lengths = [len(elem) for elem in items.values()]
    print(f"The samples tensor: {list(items.keys())} = {lengths}. Tot: {sum(lengths)}")

if __name__ == "__main__":
    options = {
        'build': mainBuildAll,
        'run': runAllSamples,
        'vtune': runAllVtuneHotspots,
        'perf': runAllPerf,
        'byline': bylineAll,
        'single': mainRunOneSample,
        'count': mainCountSamples
    }
    if len(argv) >= 2 and argv[1] in options.keys():
        options[argv[1]](argv[2:])
    else:
        print(f"expected one argument of: {list(options.keys())}")