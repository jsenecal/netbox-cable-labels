from dcim.models.cables import Cable
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .utils import render_label


@receiver(pre_save, sender=Cable)
def handle_cable_label(instance: Cable, **_kwargs):
    """
    Update cable label if not defined when Cable is updated.
    """
    if instance.pk is not None and (instance.label is None or instance.label == ""):
        instance.label = render_label(instance)


@receiver(post_save, sender=Cable)
def handle_new_cable_label(instance: Cable, created: bool, **_kwargs):
    """
    Update cable label if not defined when Cable is created.
    """
    if created and (instance.label is None or instance.label == ""):
        Cable.objects.filter(pk=instance.pk).update(label=render_label(instance))
