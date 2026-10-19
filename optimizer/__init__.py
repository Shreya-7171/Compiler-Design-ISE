"""Optimization passes for RCL three-address code."""

from optimizer.constant_folding import fold_constants
from optimizer.constant_propagation import propagate_constants

__all__ = ["fold_constants", "propagate_constants"]
