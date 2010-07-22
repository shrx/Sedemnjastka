import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User

log = logging.getLogger(__name__)

class UsersController(BaseController):

    def index(self):
        c.users = Session.query(User).order_by(User.nick_name)
        return render('/users/index.mako')

    def show(self, id):
        c.user = Session.query(User).filter(User.id==id).first()
        return render('/users/show.mako')
