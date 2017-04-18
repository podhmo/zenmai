from importlib import import_module
from ..decorators import (
    with_evaluator,
    sideeffect,
)


@with_evaluator()
@sideeffect
def from_(s, import_, evaluator):
    """
    $from: "zenmai.actions.suffix"
    import: suffix

    $suffix:
      name: foo
    """
    imported = import_module(s)
    names = import_
    if not isinstance(names, (list, tuple)):
        names = [names]
    for name in names:
        member = getattr(imported, name)
        setattr(evaluator.m, name, member)
