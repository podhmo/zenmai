# -*- coding:utf-8 -*-
from zenmai.evaluator import Evaluator
from dictknife import loading


def compile(d, module, here=None):
    evalator = Evaluator(module, d, here=here)
    return evalator.eval(d)


def compilefile(module, filename):
    loading.setup()
    d = loading.loadfile(filename)
    return compile(d, module, here=filename)
