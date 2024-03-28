.. mzdata2mat documentation master file, created by
   sphinx-quickstart on Sun Mar 24 09:46:36 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome
=======

Welcome ! ``mzdata2mat`` is a Python package which converts mzData.xml
files (version 1.05) into mat files which matlab can load and use.

|Documentation Status| |PyPI| |downloads|

Current version ``0.1.0``
-------------------------

The current version of mzdata2mat is the following : ``0.1.0``

You can see the complete changelog `here <Changelog.md>`__

Compatible hardware
-------------------

At this time, the following OSes have been tested :

macOS
~~~~~

At this time, ``macOS Sonoma 14.0`` is officially supported, other macOS
versions could be supported as long as they follow the requirements
listed below.

Windows
~~~~~~~

At this time, ``mzdata2mat`` have been tested and is supported on
``Windows 11``, no testing has been done on Windows 10 or 7 but if you
want to extend the compatibility, we are open to tester’s feedback on
thoses machines.

Requirements
------------

Other than Python
~~~~~~~~~~~~~~~~~

This package **requires node.js installed**. you can download and
install it at `nodejs.org <https://nodejs.org/en>`__. It is available
for both macOS and Windows for free.

Python version
~~~~~~~~~~~~~~

This package is compatible to any python version equal or newer than
``3.9``.

Python packages
~~~~~~~~~~~~~~~

When mzdata2mat will be installed on your system, the following packages
will also be installed (if they are not) into your Python enviuronment :

::

       pydantic>=2.6.4
       mat4py>=0.6.0
       javascript>=1!1.1.3

.. |Documentation Status| image:: https://readthedocs.org/projects/mzdata2mat/badge/?version=latest
   :target: https://mzdata2mat.readthedocs.io/en/latest/?badge=latest
.. |PyPI| image:: https://img.shields.io/pypi/v/mzdata2mat
   :target: https://pypi.org/project/mzdata2mat/
.. |downloads| image:: https://static.pepy.tech/badge/mzdata2mat/month
   :target: https://pepy.tech/project/mzdata2mat

.. toctree::
   :maxdepth: 4
   :hidden:
   :caption: Infos

   Changelog.md

.. toctree::
   :maxdepth: 4
   :hidden:
   :caption: Quickstart

   installation.md
   code-example.md
   

.. toctree::
   :maxdepth: 4
   :hidden:
   :caption: API Reference

   mzDataManager.md
   matStructure.md
   mzData.md
   mzdata2mat-verify.md
   mzDataXMLStruct.md