import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User

log = logging.getLogger(__name__)

class RankingsController(BaseController):

    def index(self):
        c.users_by_posts = Session.query(User). \
            order_by(User.num_of_posts.desc()).limit(10)
        c.users_by_topics = Session.query(User). \
            order_by(User.num_of_topics.desc()).limit(10)

        c.title = 'kralji gnoja'
        return render('/rankings.mako')
