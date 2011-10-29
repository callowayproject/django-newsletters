===============
Getting Started
===============

#. Follow instructions for :ref:`installation`.
#. Configure the :ref:`settings`, if necessary.
#. Set up the URLs in your ``urls.py``:
   
   .. code-block:: python
   
   	urlpatterns = patterns('',
   	    (r'^newsletters/', include('newsletters.urls')),
   	    # ...
   	)

#. Make sure your server can send e-mail notifications.
#. Override the :ref:`templates`, if necessary.
#. Write a signal handler for subscription and unsubscription events.