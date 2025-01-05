A CPU Sampling of the NPB-OMP Benchmark
=======================================

### About
This repository contains the results of running the NAS Parallel Benchmark for OpenMP, on a 224 logical core system, based on two NUMA nodes of the sapphire rapids architecture.
The experiments collected in this repository include executing each of the 8 benchmarks included in NAS with `2,4,8,16,32,56,64,112,128,224` threads for each of the NPB scale classes `A,B,C`. `8*11*3 = 264` experiments in total.


### Included Files
The raw stdout of all experiments is placed under the `res` directory.
The `run.py` script was used to compile and execute the experiments, the `exctract.py` script was used to find the bottom line result from each output file and the `all_res.json` file is a concise summery of all of the results.

### Hardware & Configuration
As mentioned, the hardware hardware used was x2 Intel 4th Gen (Sapphire Rapids) Xeon processors with a combined 224 logical cores.
NPB was built with the default configuration:
* The `g++ 11.4.0` system compiler.
* Flags were not changed or specified to the NPB Makefile so `-O3 -mcmodel=medium` was used (aside fomr those required for succesful compilation).
* Obviously, the scale class was re-specified for each targeted scale of `A, B, C`.
