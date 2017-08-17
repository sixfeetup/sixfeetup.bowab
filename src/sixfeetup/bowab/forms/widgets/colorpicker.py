from __future__ import absolute_import
from deform.widget import ResourceRegistry
from deform.widget import TextInputWidget


spectrum_resources = {
    "colorpicker": {'spectrum-1.1.1': {
        'js': ('sixfeetup.bowab:static/spectrum.js', ),
        'css': ('sixfeetup.bowab:static/spectrum.css', )}},
}


# set a resource registry that contains resources for the password widget
colorpicker_registry = ResourceRegistry()
colorpicker_registry.set_js_resources(
    'colorpicker', 'spectrum-1.1.1', 'sixfeetup.bowab:static/spectrum.js')
colorpicker_registry.set_css_resources(
    'colorpicker', 'spectrum-1.1.1', 'sixfeetup.bowab:static/spectrum.css')


class SpectrumColorPickerWidget(TextInputWidget):
    requirements = (('colorpicker', 'spectrum-1.1.1'), )
    template = 'sixfeetup.bowab:templates/widgets/colorpicker.pt'
    color = "#ff0000"
    default = None


def build_color_widget(color, default):
    """build a widget by passing in specific settings

    this can be used in a deferred widget binding to allow for a variety of
    widgets on a single page with different settings for color and default
    """
    return SpectrumColorPickerWidget(color=color, default=default)
