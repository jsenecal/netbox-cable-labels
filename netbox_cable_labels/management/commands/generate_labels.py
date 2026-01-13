from dcim.models.cables import Cable
from django.core.management.base import BaseCommand, CommandError

from netbox_cable_labels.utils import render_label


class Command(BaseCommand):
    """Generate labels for all cables with a missing label.
    If a label is already defined, it will not be overwritten."""

    help = "Uses the predefined template to generate labels for all cables with a missing label."

    def handle(self, *_args, **_options):
        cables_qs = Cable.objects.filter(label="")
        for cable in cables_qs:
            try:
                cable.label = render_label(cable)
                cable.save()
            except Exception as exc:  # pylint: disable=broad-except
                raise exc from CommandError(f"Error while generating label for cable {cable}")

            self.stdout.write(self.style.SUCCESS(f'Successfully updated cable "{cable}"'))
