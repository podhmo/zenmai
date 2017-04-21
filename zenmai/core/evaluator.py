from collections import OrderedDict
from zenmai.utils import (
    missing,
    isquoted,
    unquote,
)


class Evaluator:
    def eval(self, context, d):
        if hasattr(d, "keys"):
            return self.eval_dict(context, d)
        elif isinstance(d, (list, tuple)):
            return self.eval_list(context, d)
        else:
            return d

    def eval_dict(self, context, d):
        if isquoted(d):
            return unquote(d)

        method = None
        ks = []
        for k in list(d.keys()):
            if k.startswith("$"):
                if method is not None:
                    raise RuntimeError("conflicted: {!r} and {!r}".format(method, k))
                method = k
            else:
                ks.append(k)
        if method is None:
            return self._eval_args(context, d, ks)
        elif method == "$let":
            return self.eval_let_syntax(context, d, ks)
        else:
            kwargs = self._eval_args(context, d, ks)
            return self.eval_action(context, method, d, kwargs)

    def eval_list(self, context, xs):
        r = []
        has_missing = False
        for x in xs:
            v = self.eval(context, x)
            if v is missing:
                has_missing = True
            else:
                r.append(v)
        if has_missing and not r:
            return missing
        else:
            return r

    def eval_action(self, context, method, d, kwargs):
        sd = self.eval(context, d[method])

        accessor = context.accessor
        action = accessor.get_action(method[1:])
        new_kwargs = {accessor.normalize_name(k): v for k, v in kwargs.items()}
        new_kwargs.update(accessor.get_additionals(action))
        r = action(sd, **new_kwargs)
        return self.eval(context, r)

    def eval_let_syntax(self, context, d, ks):
        """
        $let:
          <var0>: <args0>
          <var1>: <args1>
          ...
        body:
          <body>

        or

        $let:
          <var0>: <args0>
          <var1>: <args1>
          ...
        <body>
        """
        bindings = d.pop("$let")
        subcontext = context.new_child(context.filename)
        for k, v in bindings.items():
            subcontext.assign(k, self.eval(context, v))
        if "body" in ks:
            return self.eval(subcontext, d["body"])
        else:
            return self.eval(subcontext, d)

    def _eval_args(self, context, d, ks):
        kwargs = OrderedDict()
        for k in ks:
            v = self.eval(context, d[k])
            if v is not missing:
                kwargs[k] = v
        return kwargs
