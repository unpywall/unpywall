Error Handling
==============

.. code-block:: python

  Unpywall.get_json(doi='not a valid doi', errors='raise')

  # Traceback (most recent call last):
  # ...

.. code-block:: python

  Unpywall.get_json(doi='not a valid doi', errors='ignore')
