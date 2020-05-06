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

   cache = UnpywallCache(timeout=2)
   Unpywall.init_cache(cache)
   original = Unpywall.get_df("10.7717/peerj.4375")
   time.sleep(1)
   record_from_cache = Unpywall.get_df("10.7717/peerj.4375") #only 1s has passed
   time.sleep(2)
   fresh_record = Unpywall.get_df("10.7717/peerj.4375") #3s have now passed, greater than the timeout (2s)

You can set a timeout (in seconds). Unpaywall sometimes updates its open access data, to reflect more accurate information now available. For long-running applications, you may want to set entries to expire in a certain amount of time, so you do not end up with outdated records.

.. code-block:: python

   Unpywall.get_df("10.7717/peerj.4375")
   time.sleep(2)
   Unpywall.get_df("10.7717/peerj.4375")

In this case, the doi will not 

.. code-block:: python

   cache = UnpywallCache()
   Unpywall.init_cache(cache)
   Unpywall.get_df("10.7717/peerj.4375", force=True)

You can also override the cache completely using the "force" option.
