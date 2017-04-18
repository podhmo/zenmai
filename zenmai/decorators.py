from .utils import missing


def with_evaluator(attr="evaluator"):
    def _with_evaluator(fn):
        if not hasattr(fn, "additionals"):
            fn.additionals = []
        fn.additionals.append(attr)
        return fn

    return _with_evaluator


def sideeffect(fn):
    def _sideeffect(*args, **kwargs):
        fn(*args, **kwargs)
        return missing

    return _sideeffect
