import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Post, Topic, User

log = logging.getLogger(__name__)

class TopicsController(BaseController):

    def show(self, id, page=1):
        c.topic = Session.query(Topic).filter(Topic.id==int(id)).first()
        c.posts = webhelpers.paginate.Page(
            Session.query(Post, User).filter(Post.user_id==User.id). \
                filter(Post.topic_id==c.topic.id). \
                order_by(Post.created_at.desc()),
            page=int(page),
            items_per_page=40)

        c.title = c.topic.full_title()
        return render('/topics/show.mako')
