from zenmai.decorators import with_evaluator
from importlib import import_module


@with_evaluator()
def from_(s, import_, evaluator):
    """
    $from: "foo.bar"
    import: bar

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
