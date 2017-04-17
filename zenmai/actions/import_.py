from zenmai.decorators import with_evaluator
from importlib import import_module


@with_evaluator()
def import_(s, evaluator, as_=None):
    """
    $import: "zenmai.actions.suffix"
    as: s

    $s.suffix:
      name: foo
    """
    imported = import_module(s)
    as_ = as_ or s.split(".")[0]
    setattr(evaluator.m, as_, imported)
