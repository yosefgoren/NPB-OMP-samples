#!/bin/pypy3
import json
from lark import Lark
from lark.tree import Tree
import sys

def tree_to_json(tree):
    if isinstance(tree, Tree):
        return {tree.data: [tree_to_json(c) for c in tree.children]}
    else:
        return str(tree)

def unshell(tgt: list):
    return tgt[0]

def strsum(tgt: list):
    return 0.0 + sum(float(num) for num in tgt) # initial 0.0 ensures float result

def process_json_tree(jtree):
    return [{key: aggregator(srcline["srcline"][i][key]) for i, (key, aggregator) in enumerate([("lineno", unshell), ("linetxt", unshell), ("runtime", strsum)])} for srcline in jtree["start"]]

def main(args):
    anotxt = sys.stdin.read()
    
    l = Lark(
    '''start: _line*

        _line: _emptyrow
            | _perc
            | _seperator
            | srcline 

        _perc: "Percent |" _SUFFIX
        _seperator: "---------------------" _SUFFIX    
        
        srcline: _srcrow runtime

        runtime: _srccont*
        
        _srccont:
            | _asmrow
            | _emptyrow

        _srcrow: ":" lineno linetxt
        _asmrow: FLOAT ":" _HEXNUM _SUFFIX
        _emptyrow: ":"

        lineno: NUMBER
        linetxt: /.+/
        
        _SUFFIX: /.+/

        _HEXNUM: /[0-9a-fA-F]+/

    %import common.WORD
    %import common.NUMBER
    %import common.FLOAT
    %ignore /\s+/
    ''')

    sys.stderr.write("starting")
    p = l.parse(anotxt)
    sys.stderr.write("done parsing")
    json_tree = tree_to_json(p)
    sys.stderr.write("done creating json")
    proc_jtree = process_json_tree(json_tree)
    sys.stderr.write("done processing json")

    with open('procano.json', 'w') as f:
        json.dump(proc_jtree, sys.stdout, indent=4)
    sys.stderr.write("done writing output file")

if __name__ == "__main__":
    main(sys.argv)
