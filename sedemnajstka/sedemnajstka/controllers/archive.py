from datetime import datetime, timedelta
import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Topic, User

from sqlalchemy import orm

log = logging.getLogger(__name__)

class ArchiveController(BaseController):

    def index(self, page=None):
        if not page:
            if 'page' in request.params:
                page = int(request.params['page'])
            else:
                page = 1

        if request.cookies.get("archive_limit"):
            c.limit = int(request.cookies.get("archive_limit"))
        else: c.limit = 25
        if request.cookies.get("archive_view"):
            c.view = request.cookies.get("archive_view")
        else: c.view = "full"

        query = Session.query(Topic, User). \
            options(orm.joinedload(User.avatar)). \
            filter(Topic.user_id==User.id). \
            order_by(Topic.last_post_created_at.desc())

        if 'from' in request.params:
            c.from_ = datetime.strptime(request.params['from'], '%Y-%m-%d')
            query = query.filter(Topic.last_post_created_at>=c.from_)
        else: c.from_ = datetime(2009, 9, 26) # Day we started
        if 'to' in request.params:
            c.to = datetime.strptime(request.params['to'], '%Y-%m-%d')
            # Defaults to 00:00 on that day, while we need end of day
            c.to += timedelta(days=1)
            query = query.filter(Topic.last_post_created_at<=c.to)
        else: c.to = datetime.now()

        c.topics = webhelpers.paginate.Page(
            query,
            page=int(page),
            items_per_page=c.limit,
            url=webhelpers.paginate.PageURL_WebOb(request))

        c.title = 'arhiv'
        return render('/archive/index.mako')
