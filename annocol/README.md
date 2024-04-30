# Purpose
The purpose of this subproject is to produce an accessible format
in which the runtime associated with each line of source code can be found.

# Usage
To achive this statistic the following steps are taken:
1. *Build Target*: Compile the target binary with debug information: `-g`.
2. *Run It*: `sudo perf record <exe-name> -o <record-name>`
3. *Extract and parse annotations*: `sudo perf annotate -i <record-name> | ./main.py > res.json`

# Means
To parse the annotations produced by `perf annotate`, the [`lark`](https://github.com/lark-parser/lark) parsing library for python is used.