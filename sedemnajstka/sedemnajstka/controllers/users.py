# -*- coding: utf-8 -*-

import logging

import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import User, Topic, Post

from GChartWrapper import HorizontalBarStack, VerticalBarStack

log = logging.getLogger(__name__)

class UsersController(BaseController):

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
        data = c.user.posts_per_dow()
        chart = HorizontalBarStack(data)
        chart.axes.type('xy')
        chart.axes.label(0, '0', '100')
        chart.axes.label(1, 'Nedelja', 'Sobota', 'Petek', 'Četrtek', 'Sreda',
                         'Torek', 'Ponedeljek')
        chart.fill('bg', 's', 'ffe495')
        chart.grid(10, 0, 10, 0)
        chart.scale(0, max(data))
        chart.size(680, 220)

        c.posts_per_dow = chart

        # Posts per hour
        data = c.user.posts_per_hour()
        chart = VerticalBarStack(data)
        chart.axes.type('yx')
        chart.axes.label(0, '0', '100')
        chart.axes.label(1, *range(0, 24))
        chart.fill('bg', 's', 'ffe495')
        chart.grid(0, 10, 10, 0)
        chart.scale(0, max(data))
        chart.size(680, 300)

        c.posts_per_hour = chart

        c.title = c.user.nick_name
        return render('/users/show.mako')
