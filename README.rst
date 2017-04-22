zenmai
========================================

.. image:: https://travis-ci.org/podhmo/zenmai.svg?branch=master
    :target: https://travis-ci.org/podhmo/zenmai


toylang on yaml or json

- code example
- command line example

code example
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
  


command line example
----------------------------------------

main.yaml

.. code-block:: yaml

  code:
    $import: ./filters.py
    as: f
  definitions:
    $let:
      nums: {$load: ./nums.yaml#/definitions/nums0/enum}
    odds:
      type: integer
      enum:
        $f.odds: {$get: nums}
    even:
      type: integer
      enum:
        $f.evens: {$get: nums}

nums.yaml

.. code-block:: yaml

  definitions:
    nums0:
      type: integer
      enum:
        [1, 2, 3, 4, 5, 6]
    nums1:
      type: integer
      enum:
        [1, 2, 3, 5, 7, 11]

filters.py

.. code-block:: python

  def odds(nums):
      return [n for n in nums if n % 2 == 1]
  
  
  def evens(nums):
      return [n for n in nums if n % 2 == 0]

run.

.. code-block:: bash

  $ zenmai examples/readme2/main.yaml

output

.. code-block:: yaml

  zenmai main.yaml
  definitions:
    odds:
      type: integer
      enum:
      - 1
      - 3
      - 5
    even:
      type: integer
      enum:
      - 2
      - 4
      - 6
  

