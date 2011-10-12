============
Installation
============

Installation is easy using ``pip`` or ``easy_install``.

.. code-block:: bash

	pip install django-newsletters

or
.. code-block:: bash

	easy_install django-newsletters


Add ``newsletters`` and ``categories`` into your ``settings.py``\ 's ``INSTALLED_APPS``:

.. code-block:: python

	INSTALLED_APPS = {
	    # ...
	    'newsletters',
	    'categories',
	}


Dependencies
************

Django-Categories