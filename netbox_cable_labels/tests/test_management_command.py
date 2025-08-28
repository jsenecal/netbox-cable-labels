"""Test the generate_labels management command."""

from django.core.management import call_command
from django.test import TestCase
from io import StringIO
from dcim.models import Site, Rack, Device, DeviceType, DeviceRole, Manufacturer, Cable, Interface


class GenerateLabelsCommandTestCase(TestCase):
    """Test the generate_labels management command."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for management command tests."""
        # Create a site
        cls.site = Site.objects.create(name="Test Site", slug="test-site")
        
        # Create manufacturer
        cls.manufacturer = Manufacturer.objects.create(
            name="Test Manufacturer",
            slug="test-manufacturer"
        )
        
        # Create device role
        cls.device_role = DeviceRole.objects.create(
            name="Test Role",
            slug="test-role"
        )
        
        # Create device type
        cls.device_type = DeviceType.objects.create(
            manufacturer=cls.manufacturer,
            model="Test Model",
            slug="test-model"
        )
        
        # Create rack
        cls.rack = Rack.objects.create(
            name="Test Rack",
            site=cls.site
        )
        
        # Create devices
        cls.device_a = Device.objects.create(
            name="Device A",
            device_type=cls.device_type,
            role=cls.device_role,
            site=cls.site,
            rack=cls.rack,
            position=1,
            face="front"
        )
        
        cls.device_b = Device.objects.create(
            name="Device B",
            device_type=cls.device_type,
            role=cls.device_role,
            site=cls.site,
            rack=cls.rack,
            position=2,
            face="front"
        )
        
        # Create interfaces
        cls.interface_a = Interface.objects.create(
            device=cls.device_a,
            name="eth0",
            type="1000base-t"
        )
        
        cls.interface_b = Interface.objects.create(
            device=cls.device_b,
            name="eth0",
            type="1000base-t"
        )

    def test_generate_labels_for_cables_without_labels(self):
        """Test that the command generates labels for cables without labels."""
        # Create cables without labels (bypass signals by using update)
        cable1 = Cable(
            label="temp",
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable1.save()
        Cable.objects.filter(pk=cable1.pk).update(label="")
        
        # Create another interface for second cable
        interface_a2 = Interface.objects.create(
            device=self.device_a,
            name="eth1",
            type="1000base-t"
        )
        interface_b2 = Interface.objects.create(
            device=self.device_b,
            name="eth1",
            type="1000base-t"
        )
        
        cable2 = Cable(
            label="temp",
            a_terminations=[interface_a2],
            b_terminations=[interface_b2]
        )
        cable2.save()
        Cable.objects.filter(pk=cable2.pk).update(label="")
        
        # Run the command
        out = StringIO()
        call_command("generate_labels", stdout=out)
        
        # Refresh cables from database
        cable1.refresh_from_db()
        cable2.refresh_from_db()
        
        # Check that labels were generated
        self.assertEqual(cable1.label, f"#{cable1.pk}")
        self.assertEqual(cable2.label, f"#{cable2.pk}")
        
        # Check command output
        output = out.getvalue()
        self.assertIn("Successfully updated cable", output)

    def test_generate_labels_skips_existing_labels(self):
        """Test that the command skips cables with existing labels."""
        # Create cable with a label
        cable = Cable(
            label="Existing Label",
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable.save()
        
        # Run the command
        out = StringIO()
        call_command("generate_labels", stdout=out)
        
        # Refresh cable from database
        cable.refresh_from_db()
        
        # Check that existing label was not changed
        self.assertEqual(cable.label, "Existing Label")
        
        # Check command output (should not mention this cable)
        output = out.getvalue()
        self.assertNotIn(str(cable), output)

    def test_generate_labels_handles_empty_queryset(self):
        """Test that the command handles the case when no cables need labels."""
        # Create cable with a label
        cable = Cable(
            label="Has Label",
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable.save()
        
        # Run the command
        out = StringIO()
        call_command("generate_labels", stdout=out)
        
        # Command should complete without errors
        # Output should be empty or minimal
        output = out.getvalue()
        self.assertNotIn("Successfully updated", output)