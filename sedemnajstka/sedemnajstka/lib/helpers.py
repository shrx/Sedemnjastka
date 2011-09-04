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

# format timedelta for use in info section
def ftd(td):
    minutes, seconds = td.seconds / 60, td.seconds % 60

    if minutes == 1: minutes_ = '1 minuto'
    elif minutes == 2: minutes_ = '2 minuti'
    elif minutes == 3 or minutes == 4: minutes_ = '%d minute' % minutes
    else: minutes_ = '%d minut' % minutes

    if seconds == 1: seconds_ = '1 sekundo'
    elif seconds == 2: seconds_ = '2 sekundi'
    elif seconds == 3 or seconds == 4: seconds_ = '%d sekunde' % seconds
    else: seconds_ = '%d sekund' % seconds

    return minutes_ + ' in ' + seconds_
