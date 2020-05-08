unpywall: Interfacing the Unpaywall Database with Python
========================================================

Welcome to unpywall’s documentation. unpywall is a Python client that interacts
with the `Unpaywall database <https://unpaywall.org/>`_, a collection of metadata
information about Open Access scholarly articles.

To get started, we recommend to read the :doc:`foreword` if you want to know more
about the project scope or further background information on Unpaywall. Otherwise,
check out the :doc:`quickstart` guide.

unpywall depends on the data analysis tool `pandas <https://pandas.pydata.org/pandas-docs/stable/index.html/>`_
and on the HTTP library `requests <https://requests.readthedocs.io/en/master/>`_.

Also, unpywall supports Python 3.5 and newer.

User's Guide
------------

.. toctree::
  :maxdepth: 2

  foreword
  installation
  quickstart
  dataformat
  errorhandling
  cache
  cli


API Reference
-------------

.. toctree::
   :maxdepth: 2

   api
