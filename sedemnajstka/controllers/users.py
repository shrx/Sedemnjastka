import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User, Topic, Post

log = logging.getLogger(__name__)

class UsersController(BaseController):

    def index(self):
        c.users = Session.query(User).order_by(User.nick_name)

        c.title = 'uporabniki'
        return render('/users/index.mako')

    def posts(self, id, page=1):
        c.user = Session.query(User).filter(User.id==int(id)).first()
        c.posts = webhelpers.paginate.Page(
            Session.query(Post).filter(Post.user_id==c.user.id). \
                order_by(Post.created_at.desc()),
            page=int(page),
            items_per_page=40)

        c.title = 'posti od ' + c.user.nick_name
        return render('/users/posts.mako')

    def topics(self, id, page=1):
        c.user = Session.query(User).filter(User.id==int(id)).first()
        c.topics = webhelpers.paginate.Page(
            Session.query(Topic).filter(Topic.user_id==c.user.id). \
                order_by(Topic.last_post_created_at.desc()),
            page=int(page),
            items_per_page=25)

        c.title = 'teme od ' + c.user.nick_name
        return render('/users/topics.mako')

    def show(self, id):
        c.user = Session.query(User).filter(User.id==id).first()

        c.title = c.user.nick_name
        return render('/users/show.mako')
