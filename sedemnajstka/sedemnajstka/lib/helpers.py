"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
import os

import pylons

from webhelpers.html.tags import *

from webhelpers.pylonslib.flash import Flash as _Flash
flash = _Flash()

# format datetime
def fdt(dt):
    return dt.strftime(pylons.config.get('datetime_format'))
