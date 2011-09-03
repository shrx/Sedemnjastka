# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
from datetime import date, timedelta
import os

import pylons

from webhelpers.html import literal
from webhelpers.html.tags import *

from webhelpers.pylonslib.flash import Flash as _Flash
flash = _Flash()

# format datetime
def fdt(dt):
    if dt.date() == date.today():
        return 'danes, ' + dt.strftime('%H:%M')
    elif dt.date() == date.today() - timedelta(days=1):
        return u'včeraj, ' + dt.strftime('%H:%M')
    else:
        return dt.strftime(pylons.config.get('datetime_format')).decode('UTF-8')
