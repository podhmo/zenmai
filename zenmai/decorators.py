def with_evaluator(attr="evaluator"):
    def _with_evaluator(fn):
        if not hasattr(fn, "additionals"):
            fn.additionals = []
        fn.additionals.append(attr)
        return fn
    return _with_evaluator
