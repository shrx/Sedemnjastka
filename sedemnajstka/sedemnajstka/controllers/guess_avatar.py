# -*- coding: utf-8 -*-
from random import choice
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Avatar, User, AvatarGuess

import sedemnajstka.lib.helpers as h

from sqlalchemy import orm
from sqlalchemy.sql import func

log = logging.getLogger(__name__)

class GuessAvatarController(BaseController):

    requires_auth = ['index', 'guessed']

    def index(self):
        c.users = Session.query(User). \
            filter(User.avatar!=None). \
            options(orm.joinedload(User.avatar)). \
            order_by(func.random()). \
            limit(8). \
            all()
        c.one = choice(c.users)
        c.avatar_guesses = Session.query(AvatarGuess). \
            options(orm.joinedload(AvatarGuess.guessed_avatar_)). \
            filter(AvatarGuess.user==session['user']). \
            order_by(AvatarGuess.created_at.desc()). \
            limit(25)

        if 'ajax' in request.params:
            return render('/guess-avatar/choice.mako')
        else:
            c.title = 'ugani avatar'
            return render('/guess-avatar/index.mako')

    def guessed(self):
        user = Session.query(User). \
            get(request.params['user_id'])
        avatar = Session.query(Avatar). \
            get(request.params['avatar_id'])

        guessed = user.avatar.id == avatar.id
        avatar_guess = AvatarGuess(guessed, avatar, session['user'])
        Session.add(avatar_guess)
        Session.commit()
        Session.refresh(session['user'])

        if 'ajax' in request.params:
            c.avatar_guess = avatar_guess
            return render('/guess-avatar/guessed-avatar.mako')
        else:
            if guessed: h.flash('Bravo, uganil/a si pravilno!')
            else: h.flash(u'Ne bo držalo.')
            redirect("/games/guess-avatar")
