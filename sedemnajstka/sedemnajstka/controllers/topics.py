import textwrap
import logging

import lxml.html
import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Post, Topic, User

from sqlalchemy import orm

log = logging.getLogger(__name__)

class TopicsController(BaseController):

    requires_auth = ['show', 'summary']

    def show(self, id, page=1):
        c.topic = Session.query(Topic).filter(Topic.id==int(id)).first()
        if not c.topic: abort(404)
        c.posts = webhelpers.paginate.Page(
            Session.query(Post, User).filter(Post.user_id==User.id). \
                options(orm.joinedload(Post.avatar)). \
                filter(Post.topic_id==c.topic.id). \
                order_by(Post.created_at),
            page=int(page),
            items_per_page=40)

        c.title = c.topic.full_title()
        return render('/topics/show.mako')

    def summary(self, id):
        post = Session.query(Post). \
            filter(Post.topic_id==id). \
            order_by(Post.created_at). \
            first()
        text = lxml.html.fromstring(post.body).text_content()
        parts = textwrap.wrap(text, 250)

        if len(parts) == 0:
            c.summary = '[&hellip;]'
        elif len(parts) == 1:
            c.summary = parts[0]
        else:
            c.summary = parts[0] + ' [&hellip;]'

        return render('/topics/summary.mako')
