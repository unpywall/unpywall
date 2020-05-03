Cache
=====

Define and Access a custom Cache
--------------------------------

.. code-block:: python

  from unpywall import Unpywall
  from unpywall.cache import UnpywallCache

  cache = UnpywallCache('custom_cache', timeout=10000)

  Unpywall.init_cache(cache)

Unpywall caches results to reduce network bandwidth and improve speed.

By default, a package-wide cache is used:

Users can also use a project-specific cache:

Users can set a timeout:

Users can also override the cache completely using the "force" option:
