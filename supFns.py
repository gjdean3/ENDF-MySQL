# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 10:46:26 2020

@author: Design
"""

def s2f(floatStr):
    return float(floatStr[0] + floatStr[1:].replace("-", "e-").replace("+", "e+"))

def s2i(floatStr):
    return int(float(floatStr[0] + floatStr[1:].replace("-", "e-").replace("+", "e+")))

def spltLn(line):
    return [line[:11],line[11:22],line[22:33],line[33:44],line[44:55],line[55:66]]