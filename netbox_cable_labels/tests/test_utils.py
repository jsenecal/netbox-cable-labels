"""Test utility functions for cable label generation."""

from django.test import TestCase, override_settings
from unittest.mock import Mock
from netbox_cable_labels.utils import render_label


class RenderLabelTestCase(TestCase):
    """Test the render_label utility function."""

    def test_render_default_template(self):
        """Test rendering with the default template."""
        # Create a mock cable object
        mock_cable = Mock()
        mock_cable.pk = 123
        
        # Render the label
        label = render_label(mock_cable)
        
        # Check the result
        self.assertEqual(label, "#123")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "Cable-{{cable.pk}}-{{cable.status}}"
            }
        }
    )
    def test_render_custom_template(self):
        """Test rendering with a custom template."""
        # Create a mock cable object
        mock_cable = Mock()
        mock_cable.pk = 456
        mock_cable.status = "connected"
        
        # Render the label
        label = render_label(mock_cable)
        
        # Check the result
        self.assertEqual(label, "Cable-456-connected")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{{cable.a_terminations.first().device.name}}-{{cable.b_terminations.first().device.name}}"
            }
        }
    )
    def test_render_complex_template(self):
        """Test rendering with a complex template accessing nested attributes."""
        # Create mock objects for the cable hierarchy
        mock_a_device = Mock()
        mock_a_device.name = "DeviceA"
        
        mock_b_device = Mock()
        mock_b_device.name = "DeviceB"
        
        mock_a_termination = Mock()
        mock_a_termination.device = mock_a_device
        
        mock_b_termination = Mock()
        mock_b_termination.device = mock_b_device
        
        mock_a_terminations = Mock()
        mock_a_terminations.first.return_value = mock_a_termination
        
        mock_b_terminations = Mock()
        mock_b_terminations.first.return_value = mock_b_termination
        
        mock_cable = Mock()
        mock_cable.a_terminations = mock_a_terminations
        mock_cable.b_terminations = mock_b_terminations
        
        # Render the label
        label = render_label(mock_cable)
        
        # Check the result
        self.assertEqual(label, "DeviceA-DeviceB")

    @override_settings(
        PLUGINS_CONFIG={
            "netbox_cable_labels": {
                "label_template": "{% if cable.length %}{{cable.length}}m{% else %}N/A{% endif %}"
            }
        }
    )
    def test_render_template_with_conditionals(self):
        """Test rendering with conditional logic in template."""
        # Test with length present
        mock_cable = Mock()
        mock_cable.length = 10
        label = render_label(mock_cable)
        self.assertEqual(label, "10m")
        
        # Test without length
        mock_cable = Mock()
        mock_cable.length = None
        label = render_label(mock_cable)
        self.assertEqual(label, "N/A")