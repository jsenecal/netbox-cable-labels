"""Test signal handlers for automatic cable labeling."""

from django.test import TestCase
from dcim.models import Site, Rack, Device, DeviceType, DeviceRole, Manufacturer, Cable, Interface
from netbox_cable_labels.utils import render_label


class CableSignalTestCase(TestCase):
    """Test automatic label generation via signals."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for cable tests."""
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

    def test_cable_label_auto_generated_on_create(self):
        """Test that a label is automatically generated when a cable is created without one."""
        cable = Cable(
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable.save()
        
        # Refresh from database
        cable.refresh_from_db()
        
        # Check that label was generated
        self.assertIsNotNone(cable.label)
        self.assertEqual(cable.label, f"#{cable.pk}")

    def test_cable_label_not_overwritten(self):
        """Test that existing labels are not overwritten."""
        custom_label = "Custom Label"
        cable = Cable(
            label=custom_label,
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable.save()
        
        # Refresh from database
        cable.refresh_from_db()
        
        # Check that custom label is preserved
        self.assertEqual(cable.label, custom_label)

    def test_cable_label_generated_on_update_when_empty(self):
        """Test that a label is generated on update if it's empty."""
        # Create cable with custom label first
        cable = Cable(
            label="temporary",
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable.save()
        
        # Clear the label and save again
        cable.label = ""
        cable.save()
        
        # Refresh from database
        cable.refresh_from_db()
        
        # Check that label was generated
        self.assertEqual(cable.label, f"#{cable.pk}")

    def test_cable_label_generated_on_update_when_none(self):
        """Test that a label is generated on update if it's None."""
        # Create cable with custom label first
        cable = Cable(
            label="temporary",
            a_terminations=[self.interface_a],
            b_terminations=[self.interface_b]
        )
        cable.save()
        
        # Set label to None and save again
        cable.label = None
        cable.save()
        
        # Refresh from database
        cable.refresh_from_db()
        
        # Check that label was generated
        self.assertEqual(cable.label, f"#{cable.pk}")