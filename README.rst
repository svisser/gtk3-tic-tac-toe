Tic Tac Toe using GTK 3, Mac OS X and Python 3.5
================================================

Implementation of Tic Tac Toe using GTK+ 3, Mac OS X and Python 3.5.

.. image:: static/screenshot.png
   :height: 434px
   :width: 352px
   :scale: 100 %
   :alt: Tic Tac Toe
   :align: left

Installation
------------

The installation steps below assume that you have installed Python 3.5 using MacPorts (https://www.macports.org):

.. code-block:: bash

    $ sudo port install python35

Install the necessary dependencies for this package:

.. code-block:: bash

    $ sudo port install gobject-introspection gtk3 py35-gobject3

It is recommended that you create a virtualenv to install this Python project locally. This is
easier when you have virtualenvwrapper installed (https://pypi.python.org/pypi/virtualenvwrapper/):

.. code-block:: bash

    $ pip install virtualenv virtualenvwrapper

When creating the virtualenv for this project you need to:

- specify the Python 3.5 interpreter for which you have installed the above dependencies, and
- ensure that the Python interpreter in the virtualenv has access to the GObject bindings installed
  for the system Python interpreter:

.. code-block:: bash

    $ mkvirtualenv gtk3-tic-tac-toe \
        --python=/opt/local/Library/Frameworks/Python.framework/Versions/3.5/bin/python3.5 \
        --system-site-packages

Lastly, install XQuartz (http://www.xquartz.org) to run X.Org X Window System on Mac OS X.

How to run
----------

You need to have XQuartz running.

You can then start the application using:

.. code-block:: bash

    python -m tictactoe
