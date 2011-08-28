# -*- coding: utf-8 -*-
from random import choice
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session

log = logging.getLogger(__name__)

class GamesController(BaseController):

    def index(self):
        c.title = 'igrice'
        return render('/games/index.mako')
