from datetime import datetime, timedelta
import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Topic, User

log = logging.getLogger(__name__)

class ArchiveController(BaseController):

    def index(self, page=None):
        if not page:
            if 'page' in request.params:
                page = int(request.params['page'])
            else:
                page = 1

        query = Session.query(Topic, User). \
            filter(Topic.user_id==User.id). \
            order_by(Topic.last_post_created_at.desc())

        if 'from' in request.params:
            c.from_ = datetime.strptime(request.params['from'], '%Y-%m-%d')
            query = query.filter(Topic.last_post_created_at>=c.from_)
        else: c.from_ = datetime(2009, 9, 26) # Day we started
        if 'to' in request.params:
            c.to = datetime.strptime(request.params['to'], '%Y-%m-%d')
            # Default to 00:00 on that day, while we need end of day
            c.to += timedelta(days=1)
            query = query.filter(Topic.last_post_created_at<=c.to)
        else: c.to = datetime.now()

        c.topics = webhelpers.paginate.Page(
            query,
            page=int(page),
            items_per_page=50,
            url=webhelpers.paginate.PageURL_WebOb(request))

        c.title = 'arhiv'
        return render('/archive.mako')
