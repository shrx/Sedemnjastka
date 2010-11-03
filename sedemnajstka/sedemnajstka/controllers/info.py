import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Info

log = logging.getLogger(__name__)

class InfoController(BaseController):

    def index(self):
        c.archive_last_run = Session.query(Info). \
            filter(Info.attribute=='archive_last_run').first().value

        c.title = 'info'
        return render('/info.mako')
