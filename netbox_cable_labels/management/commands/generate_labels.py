from django.core.management.base import BaseCommand, CommandError
from netbox_cable_labels.utils import render_label

from dcim.models.cables import Cable


class Command(BaseCommand):
    """Generate labels for all cables with a missing label.
    If a label is already defined, it will not be overwritten."""

    help = "Uses the predefined template to generate labels for all cables with a missing label."

    def handle(self, *args, **options):  # pylint: disable=unused-argument
        cables_qs = Cable.objects.filter(label="")
        for cable in cables_qs:
            try:
                cable.label = render_label(cable)
                cable.save()
            except Exception as exc:  # pylint: disable=broad-except
                raise exc from CommandError(f"Error while generating label for cable {cable}")

            self.stdout.write(
                self.style.SUCCESS('Successfully updated cable "%s"' % cable)  # pylint: disable=no-member
            )
