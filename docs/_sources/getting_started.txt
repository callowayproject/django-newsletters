
===============
Getting Started
===============

Follow instructions for installation.

Templates
=========

newsletters/base.html
---------------------

All other templates extend this template.

If your project's primary content block is not called ``content``, override ``newsletters/base.html`` and include ``{% block content %}{% endblock %}`` within the name of your primary content block.

For example, if your primary content block is called ``core_content``, override ``newsletters/base.html`` to be:

.. code-block:: django

	{% extends 'base.html' %}
	{% block core_content %}
	    {% block content %}{% endblock %}
	{% endblock %}

The change allows all the other default templates to at least work.

newsletters/list.html
---------------------

This template displays a list of available newsletters.

**Context:**

* ``newsletters`` a list of Newsletter objects
* ``form`` the form for signing up for a bunch of newsletters

newsletters/manage.html
-----------------------

This template allows bulk subscription management for a user.

**Context:**

* ``newsletters`` a list of Newsletter objects
* ``form`` the form for signing up for a bunch of newsletters
* ``messages`` a list of success or failure messages relating to the last action.

newsletters/subscribe.html
--------------------------

The successful result of the subscription to a specific newsletter.

**Context:**

* ``newsletter`` the Newsletter to which the user subscribed

newsletters/unsubscribe.html
----------------------------

The successful result of an unsubscription to a specific newsletter.

**Context:**

* ``newsletter`` the Newsletter to which the user unsubscribed

newsletters/default.html
------------------------

The default template for rendering a newsletter.
