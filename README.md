A CPU Sampling of the NPB-OMP Benchmark
=======================================

### About
This repository contains the results of running the NAS Parallel Benchmark for OpenMP, on a 224 logical core system, based on two NUMA nodes of the sapphire rapids architecture.
The experiments collected in this repository include executing each of the 8 benchmarks included in NAS with 2,4,8,16,32,64,128,224 threads. 64 experiments in total.


### Included Files
The raw stdout of all experiments is placed under the `res` directory.
The `run.py` script was used to compile and execute the experiments, the `exctract.py` script was used to find the bottom line result from each output file and the `all_res.json` file is a concise summery of all of the results.
