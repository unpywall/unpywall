Cache
=====

Define and Access a custom Cache
--------------------------------

.. code-block:: python

  from unpywall import Unpywall
  from unpywall.cache import UnpywallCache

  cache = UnpywallCache('custom_cache', timeout=1)

  Unpywall.init_cache(cache)
