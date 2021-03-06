import itertools as it
from zenmai.actions import import_  # NOQA


def suffix(d, suffix=":"):
    return {k + suffix: v for k, v in d.items()}


def ntimes(d, n=2):
    return list(it.chain.from_iterable(it.repeat(d, n)))


def inc(n):
    return n + 1


def inc2(n):
    return {"$inc": n + 1}


if __name__ == "__main__":
    import zenmai
    import sys
    from dictknife import loading

    loading.setup()  # xxx
    d = loading.loadfile(None)
    d = zenmai.compile(d, sys.modules[__name__])
    loading.dumpfile(d)
