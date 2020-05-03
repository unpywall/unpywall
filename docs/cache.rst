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

.. code-block:: python

   cache = UnpywallCache()
   Unpywall.init_cache(cache)

By default, a package-wide cache is used. 

.. code-block:: python

   cache = UnpywallCache("cache_for_analysis_script")
   Unpywall.init_cache(cache)

You can also use a project-specific cache.

.. code-block:: python

   cache = UnpywallCache(timeout=1000)
   Unpywall.init_cache(cache)

You can set a timeout (in seconds).

.. code-block:: python

   cache = UnpywallCache()
   Unpywall.init_cache(cache)
   Unpywall.get_df("10.7717/peerj.4375", force=True)

You can also override the cache completely using the "force" option.
