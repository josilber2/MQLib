"""
The MQLib module provides a python interface to the MQLib C++ library, as
described in https://pubsonline.informs.org/doi/abs/10.1287/ijoc.2017.0798 .
It can be used to access dozens of heuristics for Max-Cut and Quadratic
Unconstrained Binary Optimization (QUBO), two famous NP-hard problems.
Additionally, it provides access to a hyperheuristic, which predicts for a
given problem instance what the best-performing heuristic will be, and then
runs that one.
"""

import networkx
from numbers import Number
import numpy
import os
import _MQLib

class Instance:
    """
    Instance describes a problem instance for either Max-Cut or
    QUBO.
    """
    def __init__(self, problem, fname=None, network=None):
        """
        Construct a new 'Instance' object.
        """
        if problem != "M" and problem != "Q":
            raise ValueError("Instance problem should be \"M\" or \"Q\"")
        if fname is not None:
            self.inst = _MQLib._Inst(problem, 1, fname, None, None, None, -1)
        elif network is not None:
            if problem == "Q":
                raise ValueError("Network input only supported for Max-Cut instances")
            if not isinstance(network, networkx.classes.graph.Graph):
                raise TypeError("Network input should be a networkx graph")
            if network.is_directed():
                raise ValueError("Network should be undirected")
            mat = networkx.to_scipy_sparse_matrix(network, dtype=numpy.double)
            left = mat.nonzero()[0] + 1
            right = mat.nonzero()[1] + 1
            keep = left < right
            left = left[keep]
            right = right[keep]
            dat = mat.data[keep]
            self.inst = _MQLib._Inst(problem, 2, "", left, right, dat,
                                     network.number_of_nodes())
        else:
            raise RuntimeError("Instance needs to have a filename specified")

    def getMetrics(self):
        """
        
        """
        metrics = _MQLib.instanceMetrics(self.inst)
        return {"metrics": {x: y for x, y in zip(metrics[0], metrics[1])},
                "runtimes": {x: y for x, y in zip(metrics[2], metrics[3])}}
    
def runHeuristic(heuristic, instance, rtsec, seed=-1):
    if not isinstance(heuristic, str):
        raise TypeError("heuristic argument should be a string")
    if not isinstance(instance, Instance):
        raise TypeError("instance argument should be the Instance class")
    if not isinstance(rtsec, Number):
        raise TypeError("rtsec argument should be a number")
    if not isinstance(seed, int):
        raise TypeError("seed argument should be an integer")
    hhpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "hhdata"))
    ret = _MQLib.runHeuristic(heuristic, instance.inst, rtsec, seed, hhpath)
    return {"heuristic": ret[0],
            "instance": instance,
            "objval": ret[1],
            "solution": ret[2],
            "bestsolhistory_objvals": ret[3],
            "bestsolhistory_runtimes": ret[4]}

def getHeuristics():
    ret = _MQLib.getHeuristics()
    return {"MaxCut": {x: y for x, y in zip(ret[0], ret[1])},
            "QUBO": {x: y for x, y in zip(ret[2], ret[3])}}
