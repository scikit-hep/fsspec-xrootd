
fsspec-xrootd
=============

An xrootd implementation for fsspec.

Install
-------

.. code:: bash

    pip install fsspec-xrootd

Purpose
-------

To allow fsspec to use XRootD accessible storage systems. Install
``fsspec-xrootd`` alongside fsspec and have easy access to files stored on
XRootD servers. Once installed, fsspec will be able to work with urls with the
``root`` protocol. Only tested with Linux at this time.

The Python package depends on the XRootD client bindings directly. Running the
local integration tests also requires an ``xrootd`` server executable on
``PATH``.

.. toctree::
   :maxdepth: 3
   :titlesonly:
   :caption: Contents
   :glob:

   reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
