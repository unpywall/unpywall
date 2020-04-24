Command-Line-Interface
======================

unpywall comes also with a command-line-interface that can be used to quickly
look up a PDF or to download free full-text articles to your device.

First of all, you need to set up your credentials to access the Unpaywall service.

.. code-block:: sh

  $ export UNPAYWALL_EMAIL=nick.haupka@gmail.com

Basic commands
--------------

Obtain a PDF URL
~~~~~~~~~~~~~~~~

.. code-block:: text

  $ unpywall link 10.1038/nature12373

View a PDF
~~~~~~~~~~

.. code-block:: text

  $ unpywall view 10.1038/nature12373 -m browser

PDF Download
~~~~~~~~~~~~

.. code-block:: text

    $ unpywall download 10.1038/nature12373 -f article.pdf -p ./documents

Help
~~~~

.. code-block:: sh

  $ unpywall -h
