# -*- coding: utf-8 -*-

import bcrypt
import datetime
import logging
import time
import uuid

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from sedemnajstka.lib import mn3njalnik
from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User, Topic, Post, AvatarGuess

import sedemnajstka.lib.helpers as h

from GChartWrapper import HorizontalBarStack, VerticalBarStack
from sqlalchemy import orm

log = logging.getLogger(__name__)

days = [(1, 'Ponedeljek'),
        (2, 'Torek'),
        (3, 'Sreda'),
        (4, 'Četrtek'),
        (5, 'Petek'),
        (6, 'Sobota'),
        (7, 'Nedelja')]

class UsersController(BaseController):

    requires_auth = ['edit', 'posts']

    def index(self, content_type='text/html'):
        c.users = Session.query(User).order_by(User.nick_name)

        c.title = 'uporabniki'
        return render('/users/index.mako')

    @jsonify
    def index_json(self):
        users = Session.query(User). \
            options(orm.joinedload(User.avatar))

        usrs = {}
        for user in users:
            usrs[user.id] = {'id': user.id,
                             'nick_name': user.nick_name,
                             'num_of_posts': user.num_of_posts,
                             'num_of_topics': user.num_of_topics}
            if user.avatar:
                usrs[user.id]['avatar'] = {
                    'id': user.avatar.id,
                    'created_at': user.avatar.created_at.isoformat(),
                    'filename': user.avatar.filename,
                    'md5sum': user.avatar.md5sum,
                    'width': user.avatar.width,
                    'height': user.avatar.height
                    }

        return usrs

    def posts(self, id, page=1):
        c.user = Session.query(User).filter(User.id==int(id)).first()
        c.posts = webhelpers.paginate.Page(
            Session.query(Post, Topic). \
                options(orm.joinedload(Post.avatar)). \
                filter(Post.topic_id==Topic.id). \
                filter(Post.user_id==c.user.id). \
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
        c.user = Session.query(User). \
            options(orm.joinedload(User.avatar)). \
            get(id)
        if not c.user: abort(404)
        c.avatar_guesses_total = Session.query(AvatarGuess). \
            filter(AvatarGuess.user==c.user). \
            count()
        c.avatars_guessed = Session.query(AvatarGuess). \
            filter(AvatarGuess.user==c.user). \
            filter(AvatarGuess.guessed==True). \
            count()

        c.title = c.user.nick_name
        return render('/users/show.mako')

    def claim(self, id):
        c.user = Session.query(User).filter(User.id==id). \
            filter(User.password==None).first()
        if not c.user:
            abort(404)

        if request.method == 'POST':
            c.user.token = uuid.uuid4().get_hex()
            Session.add(c.user)
            Session.commit()

            mn3 = mn3njalnik.Mn3njalnik()
            try:
                mn3.login(config['mn3njalnik.username'],
                          config['mn3njalnik.password'])
                mn3.pm(c.user.nick_name.encode('utf-8'),
                       'Polasti se svojega racuna se danes!',
                       """
Oj, ti!

Svojega racuna na nasi strani http://sedemnajst.si se lahko polastis zdaj:

http://sedemnajst.si/users/passwd/%s

Zahteva za to sporocilo je bila podana iz sledecega IP naslova:

%s

Lep pozdrav, in ostani vedno /17/
                       """ % (c.user.token, request.environ['REMOTE_ADDR']))
                h.flash(u'Imaš ZS—velik uspeh!')
            except:
                h.flash(u'Oh ne, nekaj je šlo napak.')

        c.title = u'polasti se svojega računa'
        return render('/users/claim.mako')

    def passwd(self, token):
        c.user = Session.query(User).filter(User.token==token).first()
        if not c.user:
            abort(404)

        if request.method == 'POST':
            if request.params['passwd'] == request.params['passwd_confirm']:
                c.user.password = bcrypt.hashpw(request.params['passwd'],
                                                bcrypt.gensalt())
                c.user.token = None
                Session.add(c.user)
                Session.commit()
                h.flash(u'Uspeh—zdaj se lahko prijaviš.')
                redirect(url('login'))
            else:
                h.flash('Gesli se ne ujemata. :(')

        c.title = 'nastavi geslo'
        return render('/users/passwd.mako')

    def edit(self):
        c.user = session['user']
        if not c.user:
            abort(404)

        if request.method == 'POST':
            if 'new_passwd' in request.params:
                if bcrypt.hashpw(request.params['cur_passwd'],
                          c.user.password) == c.user.password:
                    if request.params['new_passwd'] == request. \
                            params['new_passwd_confirm']:
                        c.user.password = \
                            bcrypt.hashpw(request.params['new_passwd'],
                                          bcrypt.gensalt())
                        Session.add(c.user)
                        Session.commit()
                        h.flash(u'Podatki so bili uspešno posodobljeni.')
                    else:
                        h.flash('Gesli se ne ujemata.')
                else:
                    h.flash(u'Napačno trenutno geslo.')

        c.title = 'uredi svoje podatke'
        return render('/users/edit.mako')

    def charts(self, id, type, limit=None, start=None, end=None):
        user = Session.query(User).get(id)
        if not user: abort(404)

        if limit:
            start_date = datetime.date.today() - \
                datetime.timedelta(days=int(limit))
            end_date = None
        elif start and end:
            start = [int(i) for i in start.split('-')]
            start_date = datetime.date(start[0], start[1], start[2])
            end = [int(i) for i in end.split('-')]
            end_date = datetime.date(end[0], end[1], end[2])
        else:
            start_date = None
            end_date = None

        if type == 'ppdow':
            data = user.posts_per_dow(start_date=start_date, end_date=end_date)
            chart = HorizontalBarStack(data)
            chart.axes.type('xy')
            chart.axes.label(0, '0', '100')
            chart.axes.label(1, *reversed([i[1] for i in days]))
            chart.fill('bg', 's', 'feeebd')
            chart.grid(10, 0, 10, 0)
            chart.scale(0, max(data))
            chart.size(680, 220)
        elif type == 'pph':
            data = user.posts_per_hour(start_date=start_date, end_date=end_date)
            chart = VerticalBarStack(data)
            chart.axes.type('yx')
            chart.axes.label(0, '0', '100')
            chart.axes.label(1, *range(0, 24))
            chart.fill('bg', 's', 'feeebd')
            chart.grid(0, 10, 10, 0)
            chart.scale(0, max(data))
            chart.size(680, 300)
        else:
            abort(400)

        return chart.img()

    def avatars(self, id):
        c.user = Session.query(User). \
            options(orm.joinedload(User.avatars)). \
            get(id)
        if not c.user: abort(404)

        return render('/users/avatars.mako')
