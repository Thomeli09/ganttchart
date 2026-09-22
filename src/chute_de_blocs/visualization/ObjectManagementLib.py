# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:05:53 2025

@author: Thommes Eliott
"""

# Obect management library

# Other Lib
import copy

# Custom Lib


def ObjectCopy(Object):
    """
    Copy an object

    Get an object and return a copy of it that can 
    be modified without changing the original object
    """
    return copy.deepcopy(Object)
    