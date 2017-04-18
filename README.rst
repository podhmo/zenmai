zenmai
========================================

.. image:: https://travis-ci.org/podhmo/zenmai.svg?branch=master
    :target: https://travis-ci.org/podhmo/zenmai


toylang on yaml or json

example
----------------------------------------

main.py

.. code-block:: python

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
          age:
            $inc2: 20
      suffix: +
    suffix: "-"
  items:
    $ntimes:
      - x
      - y
    n: 3
  main:
    - $import: math
  normalized:
    ceil:
      $math.ceil: 1.5
    floor:
      $math.floor: 1.5

output

.. code-block:: yaml

  cat ./data.yaml | python ./main.py
  me:
    person+-:
      name: foo
      age: 22
  items:
  - x
  - y
  - x
  - y
  - x
  - y
  normalized:
    ceil: 2
    floor: 1
  

