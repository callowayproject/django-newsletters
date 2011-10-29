==============================
External Mailing List Managers
==============================

Upon each successful subscription or unsubscription event, Django Newsletters sends a signal. This allows you to connect outside services.

Both signals provide the same two arguments: email and newsletter. The sender is always the newsletter.

.. code-block:: python

	from newsletters.signals import subscription, unsubscription

	def print_subscription(sender, email, newsletter, *args, **kwargs):
	    print "Subscription Event!"
	    print email, newsletter

	subscription.connect(print_subscription)

	def print_unsubscription(sender, email, newsletter, *args, **kwargs):
	    print "Unsubscription Event!"
	    print email, newsletter

	unsubscription.connect(print_unsubscription)

To make sure that newsletters are available, you can also listen to newsletter create and delete signals.

.. code-block:: python

	from django.db.models.signals import post_save, pre_delete
	from newsletters.models import Newsletter

	def create_external_list(sender, instance, created, *args, **kwargs):
	    if created:
	        external_service.create_list(sender.name, sender.id)

	post_save.connect(create_external_list, sender=Newsletter)

	def delete_external_list(sender, instance, *args, **kwargs):
	    external_service.pre_delete(sender.id)

	pre_delete.connect(delete_external_list, sender=Newsletter)
