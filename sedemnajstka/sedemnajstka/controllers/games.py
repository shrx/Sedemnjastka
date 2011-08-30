# -*- coding: utf-8 -*-
from random import choice
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import t_users, t_avatar_guesses

from sqlalchemy.sql import select, func, case

log = logging.getLogger(__name__)

class GamesController(BaseController):

    def index(self):
        s = select([t_users.c.id, t_users.c.nick_name,
                    func.sum(case([(t_avatar_guesses.c.guessed==True, 1)],
                                  else_=0)),
                    func.count(t_avatar_guesses.c.guessed)],
                   from_obj=[t_avatar_guesses.join(t_users)]). \
                   group_by(t_users.c.id, t_users.c.nick_name)
        c.players = Session.execute(s)

        c.title = 'igrice'
        return render('/games/index.mako')
