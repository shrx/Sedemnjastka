# -*- coding: utf-8 -*-

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from sedemnajstka.lib.base import BaseController, render, Session
from sedemnajstka.model import Post, Quote, QuoteVote

import sedemnajstka.lib.helpers as h

from sqlalchemy import orm

log = logging.getLogger(__name__)

class QuotesController(BaseController):

    requires_auth = ['new', 'create', 'vote']

    def new(self, post):
        c.post = Session.query(Post). \
            options(orm.joinedload(Post.avatar)). \
            get(post)
        if not c.post:
            abort(404)

        # quoted already?
        if c.post.quote != None:
            h.flash(u'Ta post je že v bazi navedkov, glej:')
            redirect(url('quote', id=c.post.quote.id))

        c.title = 'dodaj navedek'
        return render('/quotes/new.mako')

    def create(self):
        post = Session.query(Post). \
            filter(Post.id==int(request.params['post'])).first()

        quote = Quote(post, session['user'])
        Session.add(quote)
        Session.commit()
        Session.refresh(session['user'])

        h.flash('Uspeh')
        redirect(url('quote', id=quote.id))

    def index(self):
        c.quotes = Session.query(Quote). \
            options(orm.joinedload_all(Quote.post, Post.avatar)). \
            order_by((Quote.upvotes-Quote.downvotes).desc())
        c.title = 'baza navedkov'
        return render('/quotes/index.mako')

    def show(self, id):
        c.quote = Session.query(Quote). \
            options(orm.joinedload_all(Quote.post, Post.avatar)). \
            get(id)
        if not c.quote:
            abort(404)
        c.title = 'navedek'
        return render('/quotes/show.mako')

    def vote(self, id, way):
        quote = Session.query(Quote).filter(Quote.id==id).first()
        if not quote:
            abort(404)

        qv = QuoteVote(quote, session['user'], way == 'up')
        Session.add(qv)
        if way == 'up':
            quote.upvotes += 1
        elif way == 'down':
            quote.downvotes += 1
        Session.add(quote)
        Session.commit()
        Session.refresh(session['user'])

        h.flash(u'Tvoj glas smo zabeležili.')
        redirect(url('quote', id=quote.id))
