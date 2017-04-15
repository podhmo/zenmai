# -*- coding:utf-8 -*-
import logging
from zenmai.evaluator import Evaluator
logger = logging.getLogger(__name__)


def compile(d, module):
    evalator = Evaluator(module)
    return evalator.eval(d)
