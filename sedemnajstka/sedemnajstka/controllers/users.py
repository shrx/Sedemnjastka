# -*- coding: utf-8 -*-

import datetime
import hashlib
import logging
import time
import uuid

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url, config
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib import mn3njalnik
from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User, Topic, Post

import sedemnajstka.lib.helpers as h

from GChartWrapper import HorizontalBarStack, VerticalBarStack

log = logging.getLogger(__name__)

days = [(1, 'Ponedeljek'),
        (2, 'Torek'),
        (3, 'Sreda'),
        (4, 'Četrtek'),
        (5, 'Petek'),
        (6, 'Sobota'),
        (7, 'Nedelja')]

months = [(1, 'Januar'),
          (2, 'Februar'),
          (3, 'Marec'),
          (4, 'April'),
          (5, 'Maj'),
          (6, 'Junij'),
          (7, 'Julij'),
          (8, 'Avgust'),
          (9, 'September'),
          (10, 'Oktober'),
          (11, 'November'),
          (12, 'December')]

# 2009 is the year the archive was started
years = [(i, i) for i in range(2009, time.localtime()[0] + 1)]

class UsersController(BaseController):

    requires_auth = ['edit']

    def index(self):
        c.users = Session.query(User).order_by(User.nick_name)

        c.title = 'uporabniki'
        return render('/users/index.mako')

    def posts(self, id, page=1):
        c.user = Session.query(User).filter(User.id==int(id)).first()
        c.posts = webhelpers.paginate.Page(
            Session.query(Post, Topic). \
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
        c.user = Session.query(User).filter(User.id==id).first()

        # Posts per DOW
        try:
            c.ppdow_start_month = int(request.params['ppdow_start_month'])
            c.ppdow_start_year = int(request.params['ppdow_start_year'])
            c.ppdow_end_month = int(request.params['ppdow_end_month'])
            c.ppdow_end_year = int(request.params['ppdow_end_year'])
        except KeyError:
            c.ppdow_start_month = 1
            c.ppdow_start_year = years[0][0]
            c.ppdow_end_month = 12
            c.ppdow_end_year = years[-1][0]

        ppdow_start_date = datetime.date(c.ppdow_start_year,
                                         c.ppdow_start_month, 1)
        ppdow_end_date = datetime.date(c.ppdow_end_year, c.ppdow_end_month, 1)

        data = c.user.posts_per_dow(start_date=ppdow_start_date,
                                    end_date=ppdow_end_date)
        chart = HorizontalBarStack(data)
        chart.axes.type('xy')
        chart.axes.label(0, '0', '100')
        chart.axes.label(1, *reversed([i[1] for i in days]))
        chart.fill('bg', 's', 'ffe495')
        chart.grid(10, 0, 10, 0)
        chart.scale(0, max(data))
        chart.size(680, 220)

        c.posts_per_dow = chart

        # Posts per hour
        try:
            c.pph_start_month = int(request.params['pph_start_month'])
            c.pph_start_year = int(request.params['pph_start_year'])
            c.pph_end_month = int(request.params['pph_end_month'])
            c.pph_end_year = int(request.params['pph_end_year'])
        except KeyError:
            c.pph_start_month = 1
            c.pph_start_year = years[0][0]
            c.pph_end_month = 12
            c.pph_end_year = years[-1][0]

        pph_start_date = datetime.date(c.pph_start_year, c.pph_start_month, 1)
        pph_end_date = datetime.date(c.pph_end_year, c.pph_end_month, 1)

        data = c.user.posts_per_hour(start_date=pph_start_date,
                                     end_date=pph_end_date)
        chart = VerticalBarStack(data)
        chart.axes.type('yx')
        chart.axes.label(0, '0', '100')
        chart.axes.label(1, *range(0, 24))
        chart.fill('bg', 's', 'ffe495')
        chart.grid(0, 10, 10, 0)
        chart.scale(0, max(data))
        chart.size(680, 300)

        c.posts_per_hour = chart

        c.months = months
        c.years = years
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
                mn3.pm(c.user.nick_name,
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
                c.user.password = hashlib.sha256(request.params['passwd']). \
                    hexdigest()
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
                if c.user.password == hashlib. \
                        sha256(request.params['cur_passwd']).hexdigest():
                    if request.params['new_passwd'] == request. \
                            params['new_passwd_confirm']:
                        c.user.password = hashlib. \
                            sha256(request.params['new_passwd']).hexdigest()
                        Session.add(c.user)
                        Session.commit()
                        h.flash(u'Podatki so bili uspešno posodobljeni.')
                    else:
                        h.flash('Gesli se ne ujemata.')
                else:
                    h.flash(u'Napačno trenutno geslo.')

        c.title = 'uredi svoje podatke'
        return render('/users/edit.mako')
