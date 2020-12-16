Quickstart
==========

Authentication
--------------

An authentification is required to use the Unpaywall Service. For that,
unpywall offers two options for authorizing the client. You can either import
``UnpywallCredentials`` which generates an environment variable or you can set
the environment variable by yourself. Both methods require an email.

.. code-block:: python

  from unpywall.utils import UnpywallCredentials

  UnpywallCredentials('nick.haupka@gmail.com')


Notice that the environment variable for authentication needs to be called
``UNPAYWALL_EMAIL``.

.. code-block:: sh

  export UNPAYWALL_EMAIL=nick.haupka@gmail.com


Pandas Integration
------------------

unpywall uses the data analysis tool
`pandas <https://pandas.pydata.org/pandas-docs/stable/index.html/>`_
for evaluating information from Unpaywall.

Query Unpaywall by DOI
----------------------

If you want to search articles by a given DOI use the method ``doi``.

.. code-block:: python

  from unpywall import Unpywall

  Unpywall.doi(dois=['10.1038/nature12373',
                     '10.1093/nar/gkr1047'])

  #    data_standard  ... best_oa_location.version
  # 0              2  ...         publishedVersion
  # 1              2  ...         publishedVersion

  # [2 rows x 32 columns]


You can track the progress of your API call by setting the parameter
``progress`` to True. This is especially useful for estimating the time
required.

.. code-block:: python

  Unpywall.doi(dois=['10.1038/nature12373',
                     '10.1093/nar/gkr1047'],
               progress=True)

  # |=========================                        | 50%


Calculate the fraction of OA types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

  df = Unpywall.doi(dois=['10.1038/nature12373',
                          '10.1093/nar/gkr1047'])

  df.oa_status.value_counts(normalize=True)
  # green    0.5
  # gold     0.5
  # Name: oa_status, dtype: float64
