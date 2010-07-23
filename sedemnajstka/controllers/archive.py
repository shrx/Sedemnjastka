import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Topic, User

log = logging.getLogger(__name__)

class ArchiveController(BaseController):

    def index(self, page=1):
        c.topics = webhelpers.paginate.Page(
            Session.query(Topic, User).filter(Topic.user_id==User.id). \
                order_by(Topic.last_post_created_at.desc()),
            page=int(page),
            items_per_page=50)

        c.title = 'arhiv'
        return render('/archive.mako')
