from zenmai.actions import load  # NOQA


if __name__ == "__main__":
    import zenmai
    import sys
    from dictknife import loading
    d = zenmai.compilefile(sys.modules[__name__], sys.argv[1])
    loading.dumpfile(d)
