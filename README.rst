zenmai
========================================

toylang on yaml or json

example
----------------------------------------

main.py

.. code-block:: python

  import itertools as it
  
  
  def suffix(d, suffix=":"):
      return {k + suffix: v for k, v in d.items()}
  
  
  def ntimes(d, n=2):
      return list(it.chain.from_iterable(it.repeat(d, n)))
  
  
  if __name__ == "__main__":
      import zenmai
      import sys
      from dictknife import loading
  
      loading.setup()  # xxx
      d = loading.loadfile(None)
      d = zenmai.compile(d, sys.modules[__name__])
      loading.dumpfile(d)

run.

.. code-block:: bash

  $ cat examples/readme/data.yaml > examples/readme/main.py

data.yaml

.. code-block:: yaml

  me:
    $suffix:
      $suffix:
        person:
          name: foo
          age: 20
      suffix: +
    suffix: +
  items:
    $ntimes:
      - x
      - y
    n: 3

output

.. code-block:: yaml

  me:
    person++:
      name: foo
      age: 20
  items:
  - x
  - y
  - x
  - y
  - x
  - y
  

