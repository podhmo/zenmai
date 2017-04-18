from zenmai.actions import load  # NOQA


if __name__ == "__main__":
    import zenmai
    import sys
    from dictknife import loading
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    srcfile = sys.argv[1]
    d = zenmai.compilefile(sys.modules[__name__], srcfile)
    loading.dumpfile(d)
