from collections import OrderedDict
from .utils import missing
import keyword


class Evaluator:
    def __init__(self, m):
        self.m = m
        self.accessor = Accessor(self)  # todo: reify

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
                    if v is not missing:
                        kwargs[k] = v
            if method is None:
                return kwargs
            return self.eval(self.apply(method[1:], self.eval(d[method]), kwargs=kwargs))
        elif isinstance(d, (list, tuple)):
            r = []
            has_missing = False
            for x in d:
                v = self.eval(x)
                if v is missing:
                    has_missing = True
                else:
                    r.append(v)
            if has_missing and not r:
                return missing
            else:
                return r
        else:
            return d

    def apply(self, name, d, kwargs):
        path = name.split(".")
        method = self.m
        for p in path[:-1]:
            method = getattr(method, p)
        method = getattr(method, self.accessor.normalize_name(path[-1]))
        new_kwargs = {self.accessor.normalize_name(k): v for k, v in kwargs.items()}
        new_kwargs.update(self.accessor.get_additionals(method))
        return method(d, **new_kwargs)


class Accessor(object):
    def __init__(self, evaluator):
        self.evaluator = evaluator

    def get_additionals(self, method):
        additionals = getattr(method, "additionals", [])
        return [(name, getattr(self, name)) for name in additionals]

    def normalize_name(self, name):
        if keyword.iskeyword(name):
            return name + "_"
        else:
            return name
