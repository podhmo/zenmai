from importlib import import_module
from ..decorators import (
    with_evaluator,
    sideeffect,
)


@with_evaluator()
@sideeffect
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
