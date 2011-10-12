=============
Subscriptions
=============

Basic API workflow
==================

**index:** Allows new users to sign up for newsletters

**user newsletter management:** Allows a user change the subscription status of all the newsletters. This does not do atomic changes. It changes the status for all newsletters at once.

**newsletter detail:** Provides the HTML of the newsletter. Renders the first template it finds in the order: 

#. ``newsletters/<newsletter-slug>.html``
#. ``newsletters/category.html``
#. ``NEWSLETTERS_SETTINGS['DEFAULT_TEMPLATE']``

The template will have the following variables in the context:

* ``newsletter:`` The Newsletter object
* ``category:`` The Category object of the newsletter
* ``ads:`` A list of Advertisement objects scheduled for this newsletter


Management of newsletter subscriptions is managed through a simple API:


A ``GET`` or ``POST`` request to the **newsletter index page** returns a page with a form for signing up, a list of the available newsletters with checkboxes, and a field to enter the e-mail address.

If the request also includes ``format=JSON``, the newsletter list and signup URL are sent in ``JSON`` format.

A ``GET`` or ``POST`` request to the newsletter index page with the parameter ``u`` and the users e-mail address (``u=username@example.com``) will redirect to the **newsletter manage page,** which includes the list of newsletters that the e-mail address is subscribed and allows the user to modify the list.

A summary is provided below:

============   ======   ===========   ========================================
Request Type   Has u    has format    Result
============   ======   ===========   ========================================
GET            No       No            HTML newsletter sign up form
GET            Yes      No            Redirect to manage page for user
GET            No       Yes           JSON newsletter list and sign up URL
GET            Yes      Yes           Redirect to manage page for user
POST           No       No            HTML newsletter sign up form
POST           Yes      No            Redirect to manage page for user
POST           No       Yes           JSON newsletter list and sign up URL
POST           Yes      Yes           Redirect to manage page for user
============   ======   ===========   ========================================





Subscriptions
=============

Here is an example subscription landing page.

.. image:: images/subscriptionform.png
   :alt: An example subscription landing page

Start
-----

#. User goes to the mailing list landing page.

#. They have the choice to manage their newsletter subscriptions (returning user), or sign up for newsletters (new user)

New Users
---------

#. A list of available newsletters with checkboxes, a text field for their e-mail address, and a submit button are available.

#. The user enters their email address, checks the appropriate newsletters and submits the form.

#. If there are errors in the submission, the form will appear again with an error message.

#. If there are no errors, a success page is displayed informing the user a confirmation email was sent.

Returning Users
---------------

#. User submits their email address to ``./manage/``

#. The form shows all currently subscribed newsletters with checked checkboxes.

#. The user can check or uncheck the boxes to subscribe or unsubscribe from the newsletters.

#. Submission of the form will either provide information regarding errors in the form or displays a success page informing the user a confirmation email was sent.

Confirmation
------------

#. The confirmation email tells the user that there was a change to their newsletter subscriptions. It contains a link to manage their subscriptions if there was an error.