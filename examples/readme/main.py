import itertools as it


def suffix(d, suffix=":"):
    return {k + suffix: v for k, v in d.items()}


def ntimes(d, n=2):
    return list(it.chain.from_iterable(it.repeat(d, n)))

if __name__ == "__main__":
    import argparse
    import sys
    import zenmai
    from dictknife import loading
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst", default=None)
    parser.add_argument("src", default=None)

    args = parser.parse_args()

    loading.setup()  # xxx
    d = loading.loadfile(args.src)
    d = zenmai.compile(d, sys.modules[__name__])
    loading.dumpfile(d, args.dst)
