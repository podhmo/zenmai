from importlib import import_module
from ..decorators import (
    with_context,
    sideeffect,
)


@with_context
@sideeffect
def import_(s, context, as_=None):
    """
    $import: "zenmai.actions.suffix"
    as: s

    $s.suffix:
      name: foo
    """
    imported = import_module(s)
    as_ = as_ or s.split(".")[0]
    context.assign(as_, imported)
