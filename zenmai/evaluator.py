from collections import OrderedDict


class Evaluator:
    def __init__(self, m):
        self.m = m

    def eval(self, d):
        if hasattr(d, "keys"):
            method = None
            kwargs = OrderedDict()
            for k in list(d.keys()):
                if k.startswith("$"):
                    if method is not None:
                        raise RuntimeError("conflicted: {!r} and {!r}".format(method, k))
                    method = k
                else:
                    v = self.eval(d[k])
                    kwargs[k] = v
            if method is None:
                return kwargs
            return self.apply(method[1:], self.eval(d[method]), kwargs=kwargs)
        elif isinstance(d, (list, tuple)):
            return [self.eval(x) for x in d]
        else:
            return d

    def apply(self, name, d, kwargs):
        method = getattr(self.m, name)
        return method(d, **kwargs)
