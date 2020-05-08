Error Handling
==============

A number of errors can occur when accessing Unpaywall, including:
    Network errors
    Invalid DOIs

.. code-block:: python

  Unpywall.get_json(doi='not a valid doi', errors='raise')

  # Traceback (most recent call last):
  # ...

Where any error should be fatal, you can use the 'raise' option. For example, if you are doing data analysis, you should use this option for reproducibility.

.. code-block:: python

  Unpywall.get_json(doi='not a valid doi', errors='ignore')

If errors can be tolerated, you can use the 'ignore' option. For example, if you are experimenting with Unpaywall and its API, or building a system where missing data is not a big problem, this may be the option for you.
