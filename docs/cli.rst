Command-Line-Interface
======================

unpywall comes with a command-line-interface that can be used to quickly
look up a PDF or to download free full-text articles to your device.

First of all, you need to set up your credentials to access the Unpaywall service.

.. code-block:: sh

  $ export UNPAYWALL_EMAIL=nick.haupka@gmail.com

Basic commands
--------------

Obtain a PDF URL
~~~~~~~~~~~~~~~~

Retrieve the URL of a PDF for a given DOI with the following command.

.. code-block:: text

  $ unpywall link 10.1038/nature12373

View a PDF
~~~~~~~~~~

If you want to view a PDF in your Browser or on your system use ``view``.

.. code-block:: text

  $ unpywall view 10.1038/nature12373 -m browser

PDF Download
~~~~~~~~~~~~

Use ``download`` if you want to store a PDF on your machine.

.. code-block:: text

    $ unpywall download 10.1038/nature12373 -f article.pdf -p ./documents

Help
~~~~

You can always use ``help`` to open a description for the provided functions.

.. code-block:: sh

  $ unpywall -h
