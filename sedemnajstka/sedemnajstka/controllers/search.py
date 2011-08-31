import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Topic, Post, User

from sqlalchemy import orm
from sqlalchemy.sql import func

log = logging.getLogger(__name__)

class SearchController(BaseController):

    requires_auth = ['index']

    def index(self):
        current_page = 'page' in request.params \
            and int(request.params['page']) or 1
        q = request.params['q']

        c.results = webhelpers.paginate.Page(
            Session.query(Post, Topic, User). \
                options(orm.joinedload(Post.avatar)). \
                filter(Topic.id==Post.topic_id). \
                filter(User.id==Post.user_id). \

                filter('tsv @@ plainto_tsquery(:terms)'). \
                params(terms=q). \

                add_column(func.ts_headline('pg_catalog.simple',
                                            Post.body,
                                            func.plainto_tsquery(q),
                                            'HighlightAll=TRUE, ' \
                                            'StartSel=<strong>, ' \
                                            'StopSel=</strong>')). \

                order_by(Post.created_at.desc()),
            page=current_page,
            items_per_page=40,
            url=webhelpers.paginate.PageURL_WebOb(request))

        c.title = 'rezultati iskanja'
        return render('/search.mako')
