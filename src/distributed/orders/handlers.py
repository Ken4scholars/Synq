from django.dispatch import receiver

from distributed.services.synq import Synq
from . import signals


@receiver(signals.created)
def handle_created(sender, id, number, name, **kwargs):
    with Synq() as synq:
        synq.create_order(pk=id, number=number, name=name)


@receiver(signals.updated)
def handle_updated(sender, id, number, name, **kwargs):
    with Synq() as synq:
        synq.update_order(pk=id, number=number, name=name)


@receiver(signals.deleted)
def handle_deleted(sender, id, **kwargs):
    with Synq() as synq:
        synq.delete_order(pk=id)