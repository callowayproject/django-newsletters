
========
Settings
========

.. contents::
   :local:


DEFAULT_SETTINGS
================

.. code-block:: python

	DEFAULT_SETTINGS = {
	    'POSITIONS': (
	        (1, 'Leaderboard'),
	        (2, 'Medium Rectangle'),
	        (3, 'Button 1 (1)'),
	        (4, 'Button 1 (2)'),
	    ),
	    'DEFAULT_TEMPLATE': 'newsletters/default.html',
	    'ADVERTISEMENT_STORAGE': settings.DEFAULT_FILE_STORAGE,
	}


POSITIONS
=========

Advertising positions available for scheduling. Consists of a tuple of ``int`` and ``string`` tuples.

**Default:** ``((1, 'Leaderboard'), (2, 'Medium Rectangle'), (3, 'Button 1 (1)'), (4, 'Button 1 (2)'),)``

DEFAULT_TEMPLATE
================

The default template to use when rendering a newsletter. The app looks for templates in the following order:

#. ``newsletters/<newsletter-slug>.html``
#. ``newsletters/<category-slug>.html``
#. ``DEFAULT_TEMPLATE``

**Default:** ``newsletters/default.html``


ADVERTISEMENT_STORAGE
=====================

Storage engine to use when saving advertising images.

**Default:** settings.DEFAULT_FILE_STORAGE
