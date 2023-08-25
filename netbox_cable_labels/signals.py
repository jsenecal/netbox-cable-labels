from .utils import render_label
from dcim.models.cables import Cable
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


@receiver(pre_save, sender=Cable)
def handle_cable_label(instance: Cable, **kwargs):  # pylint: disable=unused-argument
    """
    Update cable label if not defined when Cable is updated.
    """
    if instance.pk is not None and (instance.label is None or instance.label == ""):
        instance.label = render_label(instance)


@receiver(post_save, sender=Cable)
def handle_new_cable_label(instance: Cable, created: bool, **kwargs):  # pylint: disable=unused-argument
    """
    Update cable label if not defined when Cable is created.
    """
    if created and (instance.label is None or instance.label == ""):
        Cable.objects.filter(pk=instance.pk).update(label=render_label(instance))
