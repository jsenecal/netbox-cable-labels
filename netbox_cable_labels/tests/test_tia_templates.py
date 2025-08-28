"""Test TIA-606-C compliant template rendering."""

from django.test import TestCase, override_settings
from unittest.mock import Mock, MagicMock
from netbox_cable_labels.utils import render_label


class TIA606CTemplateTestCase(TestCase):
    """Test various TIA-606-C compliant templates."""

    def setUp(self):
        """Set up mock cable object with full NetBox-like structure."""
        # Create mock site objects
        self.mock_site_a = Mock()
        self.mock_site_a.name = "NYC"
        
        self.mock_site_b = Mock()
        self.mock_site_b.name = "NYC"
        
        # Create mock location objects
        self.mock_location_a = Mock()
        self.mock_location_a.name = "Floor2"
        
        self.mock_location_b = Mock()
        self.mock_location_b.name = "Floor1"
        
        # Create mock rack objects
        self.mock_rack_a = Mock()
        self.mock_rack_a.name = "R1A"
        
        self.mock_rack_b = Mock()
        self.mock_rack_b.name = "R2B"
        
        # Create mock manufacturer
        self.mock_manufacturer_a = Mock()
        self.mock_manufacturer_a.name = "Cisco"
        
        self.mock_manufacturer_b = Mock()
        self.mock_manufacturer_b.name = "HPE"
        
        # Create mock device type
        self.mock_device_type_a = Mock()
        self.mock_device_type_a.manufacturer = self.mock_manufacturer_a
        
        self.mock_device_type_b = Mock()
        self.mock_device_type_b.manufacturer = self.mock_manufacturer_b
        
        # Create mock device objects
        self.mock_device_a = Mock()
        self.mock_device_a.name = "SW01"
        self.mock_device_a.site = self.mock_site_a
        self.mock_device_a.location = self.mock_location_a
        self.mock_device_a.rack = self.mock_rack_a
        self.mock_device_a.position = 42
        self.mock_device_a.face = "front"
        self.mock_device_a.device_type = self.mock_device_type_a
        
        self.mock_device_b = Mock()
        self.mock_device_b.name = "SW02"
        self.mock_device_b.site = self.mock_site_b
        self.mock_device_b.location = self.mock_location_b
        self.mock_device_b.rack = self.mock_rack_b
        self.mock_device_b.position = 10
        self.mock_device_b.face = "rear"
        self.mock_device_b.device_type = self.mock_device_type_b
        
        # Create mock termination objects
        self.mock_termination_a = Mock()
        self.mock_termination_a.device = self.mock_device_a
        self.mock_termination_a.name = "gi1/0/1"
        
        self.mock_termination_b = Mock()
        self.mock_termination_b.device = self.mock_device_b
        self.mock_termination_b.name = "eth1/1"
        
        # Create mock terminations manager
        self.mock_a_terminations = Mock()
        self.mock_a_terminations.first.return_value = self.mock_termination_a
        
        self.mock_b_terminations = Mock()
        self.mock_b_terminations.first.return_value = self.mock_termination_b
        
        # Create mock cable object
        self.mock_cable = Mock()
        self.mock_cable.pk = 123
        self.mock_cable.type = "CAT6A"
        self.mock_cable.status = "connected"
        self.mock_cable.color = "blue"
        self.mock_cable.length = 10
        self.mock_cable.length_unit = "m"
        self.mock_cable.a_terminations = self.mock_a_terminations
        self.mock_cable.b_terminations = self.mock_b_terminations

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.rack.name}}-{{cable.a_terminations.first().device.position}}{{cable.a_terminations.first().device.face|first|upper}}/{{cable.b_terminations.first().device.rack.name}}-{{cable.b_terminations.first().device.position}}{{cable.b_terminations.first().device.face|first|upper}}/{{cable.type|default('UTP')}}/C{{'{:05d}'.format(cable.pk)}}"
            }
        }
    )
    def test_basic_tia_606c_template(self):
        """Test basic TIA-606-C rack-based template."""
        label = render_label(self.mock_cable)
        self.assertEqual(label, "R1A-42F/R2B-10R/CAT6A/C00123")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.site.name}}-{{cable.a_terminations.first().device.name}}/{{cable.b_terminations.first().device.site.name}}-{{cable.b_terminations.first().device.name}}/{{cable.type|default('CAT6')}}/{{cable.pk}}"
            }
        }
    )
    def test_site_based_template(self):
        """Test site-based TIA-606-C template."""
        label = render_label(self.mock_cable)
        self.assertEqual(label, "NYC-SW01/NYC-SW02/CAT6A/123")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{%- set a_term = cable.a_terminations.first() -%}{%- set b_term = cable.b_terminations.first() -%}{{a_term.device.site.name|upper}}-{{a_term.device.rack.name ~ ':' ~ a_term.device.name}}-{{a_term.name}}/{{b_term.device.site.name|upper}}-{{b_term.device.rack.name ~ ':' ~ b_term.device.name}}-{{b_term.name}}{%- if cable.length %}/{{cable.length}}m{% endif %}/ID{{'{:06d}'.format(cable.pk)}}"
            }
        }
    )
    def test_detailed_location_template(self):
        """Test detailed location template with port information."""
        label = render_label(self.mock_cable)
        self.assertEqual(label, "NYC-R1A:SW01-gi1/0/1/NYC-R2B:SW02-eth1/1/10m/ID000123")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.location.name}}.{{cable.a_terminations.first().device.rack.name}}.{{cable.a_terminations.first().name}}/{{cable.b_terminations.first().device.location.name}}.{{cable.b_terminations.first().device.rack.name}}.{{cable.b_terminations.first().name}}/{{cable.type}}/{{cable.pk}}"
            }
        }
    )
    def test_building_floor_room_template(self):
        """Test building/floor/room based template."""
        label = render_label(self.mock_cable)
        self.assertEqual(label, "Floor2.R1A.gi1/0/1/Floor1.R2B.eth1/1/CAT6A/123")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{% set a = cable.a_terminations.first() %}{% set b = cable.b_terminations.first() %}{{a.device.device_type.manufacturer.name[:3]|upper}}{{a.device.name}}-{{a.name}}/{{b.device.device_type.manufacturer.name[:3]|upper}}{{b.device.name}}-{{b.name}}/{{cable.type|default('CAT6')}}/{{cable.color[:3]|upper if cable.color else 'BLU'}}"
            }
        }
    )
    def test_patch_panel_focused_template(self):
        """Test patch panel focused template with manufacturer abbreviation."""
        label = render_label(self.mock_cable)
        self.assertEqual(label, "CISSW01-gi1/0/1/HPESW02-eth1/1/CAT6A/BLU")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.name}}-{{cable.a_terminations.first().name}} to {{cable.b_terminations.first().device.name}}-{{cable.b_terminations.first().name}}"
            }
        }
    )
    def test_simple_descriptive_template(self):
        """Test simple descriptive template."""
        label = render_label(self.mock_cable)
        self.assertEqual(label, "SW01-gi1/0/1 to SW02-eth1/1")

    def test_template_with_missing_attributes(self):
        """Test template handling when some attributes are missing."""
        # Create cable with minimal data
        mock_device_minimal = Mock()
        mock_device_minimal.name = "Device1"
        mock_device_minimal.site = None
        mock_device_minimal.rack = None
        mock_device_minimal.location = None
        
        mock_termination_minimal = Mock()
        mock_termination_minimal.device = mock_device_minimal
        mock_termination_minimal.name = "port1"
        
        mock_terminations = Mock()
        mock_terminations.first.return_value = mock_termination_minimal
        
        mock_cable_minimal = Mock()
        mock_cable_minimal.pk = 456
        mock_cable_minimal.type = None
        mock_cable_minimal.color = None
        mock_cable_minimal.length = None
        mock_cable_minimal.a_terminations = mock_terminations
        mock_cable_minimal.b_terminations = mock_terminations
        
        with override_settings(
            PLUGINS_CONFIG={
                "netbox_cable_labels": {
                    "label_template": "{{cable.a_terminations.first().device.name}}/{{cable.b_terminations.first().device.name}}/{{cable.type if cable.type else 'UNK'}}/{{cable.pk}}"
                }
            }
        ):
            label = render_label(mock_cable_minimal)
            self.assertEqual(label, "Device1/Device1/UNK/456")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{% if 'fiber' in cable.type|lower or 'sm' in cable.type|lower %}FO-{% endif %}{{cable.a_terminations.first().device.rack.name}}-{{cable.a_terminations.first().name}}/{{cable.b_terminations.first().device.rack.name}}-{{cable.b_terminations.first().name}}/{{cable.type|upper}}"
            }
        }
    )
    def test_fiber_optic_template(self):
        """Test fiber optic cable template with conditional prefix."""
        # Test with fiber cable
        self.mock_cable.type = "SM-OS2"
        label = render_label(self.mock_cable)
        self.assertEqual(label, "FO-R1A-gi1/0/1/R2B-eth1/1/SM-OS2")
        
        # Test with copper cable
        self.mock_cable.type = "CAT6A"
        label = render_label(self.mock_cable)
        self.assertEqual(label, "R1A-gi1/0/1/R2B-eth1/1/CAT6A")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.rack.name}}-{{'{:02d}'.format(cable.a_terminations.first().device.position)}}/{{cable.b_terminations.first().device.rack.name}}-{{'{:02d}'.format(cable.b_terminations.first().device.position)}}"
            }
        }
    )
    def test_position_formatting(self):
        """Test position formatting with zero padding."""
        self.mock_device_b.position = 5
        label = render_label(self.mock_cable)
        self.assertEqual(label, "R1A-42/R2B-05")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.location.name|default(cable.a_terminations.first().device.site.name)}}.{{cable.a_terminations.first().device.name}}"
            }
        }
    )
    def test_fallback_values(self):
        """Test template with fallback values using default filter."""
        # With location
        label = render_label(self.mock_cable)
        self.assertIn("Floor2.SW01", label)
        
        # Without location (should fall back to site)
        self.mock_device_a.location = None
        label = render_label(self.mock_cable)
        self.assertIn("NYC.SW01", label)