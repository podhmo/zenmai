from dictknife import deepmerge
from collections import OrderedDict


def concat(ds):
    """
    $concat:
      - name: foo
      - age: 10
    """
    return deepmerge(OrderedDict(), *ds)
