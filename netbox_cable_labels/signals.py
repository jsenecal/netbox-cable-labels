from .utils import render_label
from dcim.models.cables import Cable
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=Cable)
def handle_cable_label(instance: Cable, **kwargs):  # pylint: disable=unused-argument
    """
    Update cable label if not defined when Cable is created or updated.
    """
    if instance.label is None or instance.label == "":
        instance.label = render_label(instance)
