# -*- coding:utf-8 -*-
from zenmai.core.evaluator import Evaluator
from zenmai.core.context import Context
from zenmai.core.loader import Loader
from dictknife import loading


def compile(d, module, filename=None):
    evalator = Evaluator()
    loader = Loader(d, rootfile=filename)
    context = Context(module, loader, evalator, filename=filename)
    return evalator.eval(context, d)


def compilefile(module, filename):
    loading.setup()
    d = loading.loadfile(filename)
    return compile(d, module, filename=filename)
