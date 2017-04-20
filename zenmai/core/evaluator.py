from collections import OrderedDict
from zenmai.utils import (
    missing,
    isquoted,
    unquote,
)


class Evaluator:
    def eval(self, context, d):
        if hasattr(d, "keys"):
            if isquoted(d):
                return unquote(d)

            method = None
            kwargs = OrderedDict()
            for k in list(d.keys()):
                if k.startswith("$"):
                    if method is not None:
                        raise RuntimeError("conflicted: {!r} and {!r}".format(method, k))
                    method = k
                else:
                    v = self.eval(context, d[k])
                    if v is not missing:
                        kwargs[k] = v
            if method is None:
                return kwargs
            sd = self.eval(context, d[method])
            r = self.apply(context, method[1:], sd, kwargs=kwargs)
            return self.eval(context, r)
        elif isinstance(d, (list, tuple)):
            r = []
            has_missing = False
            for x in d:
                v = self.eval(context, x)
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

    def apply(self, context, name, d, kwargs):
        accessor = context.accessor
        action = accessor.get_action(name)
        new_kwargs = {accessor.normalize_name(k): v for k, v in kwargs.items()}
        new_kwargs.update(accessor.get_additionals(action))
        return action(d, **new_kwargs)
