# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session

log = logging.getLogger(__name__)

class CollageController(BaseController):

    def index(self):
        c.title = u'kolaž'
        return render('/collage.mako')
