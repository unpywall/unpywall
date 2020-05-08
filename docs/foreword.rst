Foreword
========

What is Unpaywall?
------------------

`Unpaywall <https://unpaywall.org/>`_ searches for open access full-text copies
of scholarly literature and offers various open-source tools to work with them.
More specifically, Unpaywall, a non-profit service builded and maintained by
`Our Research <https://ourresearch.org/>`_, provides metadata about free-to-read
versions of scientific publications such as research papers and journal articles [1]_.

These metadata information is stored in a large database that contains several
million records. The data can be queried either using a provided
`database snapshot <https://unpaywall.org/products/snapshot>`_ which is around
100GB in size, or via the Unpaywall `REST API <https://unpaywall.org/products/api>`_.

The REST API returns a JSON data structure which contains information about a
Digital Object Identifier (DOI) like open access status, title and full-text link.
For a detailed schema description see :doc:`dataformat`.

Project background
------------------

We use Unpaywall in different contexts. On the one hand, we use Unpaywall to
examine the proportion of open access articles in journals and repositories. For
that, we provide a `pandas <https://pandas.pydata.org/pandas-docs/stable/index.html/>`_
integration to easily create DataFrames that can be used for bibliometric
research. Besides, our package provides convenient functions for literature
mining such as downloading pdf handles or retrieving full-text links.

Our Goal is to develop a tiny Python wrapper around the Unpaywall REST API to
make interactions between Python and Unpaywall even more comfortable and less
time consuming as it already is.

.. rubric:: References

.. [1] https://peerj.com/articles/4375/
