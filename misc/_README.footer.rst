config loader
----------------------------------------

using zenmai as config loader.

.. code-block:: python

  from zenma.loader import load

  with open("config.yaml") as rf:
      d = load(rf)

