from dictknife import deepmerge


def concat(ds, override=False):
    """
    $concat:
      - name: foo
      - age: 10
    """
    return deepmerge(*ds, override=override)
