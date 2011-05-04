# -*- coding: utf-8 -*-

import bcrypt
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User

import sedemnajstka.lib.helpers as h

log = logging.getLogger(__name__)

class AuthController(BaseController):

    def login(self):
        if request.method == 'POST':
            user = Session.query(User). \
                filter(User.nick_name==request.params['nick_name']) . \
                filter(User.password!=None).first()

            if user and bcrypt.hashpw(request.params['password'],
                                      user.password) == user.password:
                session['user'] = user
                session.save()
                if 'return_to' in session:
                    to = session['return_to']
                    del session['return_to']
                    session.save()
                    redirect(to)
                elif 'return_to' in request.params:
                    redirect(request.params['return_to'])
                else:
                    redirect('/')
            else:
                h.flash(u'Sorči, to ni nobena kombinacija uporabniškega imena' +
                        'in gesla, ki bi bila meni znana.')

        c.title = 'prijava'
        return render('/auth/login.mako')

    def logout(self):
        if 'user' in session:
            del session['user']
            session.save()
        redirect('/')
