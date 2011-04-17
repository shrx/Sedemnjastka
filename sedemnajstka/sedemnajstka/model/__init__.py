"""The application's model objects"""
import datetime

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql import select, func, and_

from sedemnajstka.model import meta


t_info = None
t_posts = None
t_quotes = None
t_quote_votes = None
t_topics = None
t_users = None


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.Base.metadata.bind = engine

    global t_info, t_posts, t_quotes, t_quote_votes, t_topics, t_users
    t_info = sa.Table('info', meta.Base.metadata, autoload=True)
    t_posts = sa.Table('posts', meta.Base.metadata, autoload=True)
    t_quotes = sa.Table('quotes', meta.Base.metadata, autoload=True)
    t_quote_votes = sa.Table('quote_votes', meta.Base.metadata, autoload=True)
    t_topics = sa.Table('topics', meta.Base.metadata, autoload=True)
    t_users = sa.Table('users', meta.Base.metadata, autoload=True)

    orm.mapper(Info, t_info)
    orm.mapper(Post, t_posts, properties={
            'user': orm.relationship(User, backref='posts'),
            'topic': orm.relationship(Topic, backref='posts')})
    orm.mapper(Quote, t_quotes, properties={
            'post': orm.relationship(Post, uselist=False, backref=orm.backref('quote', uselist=False)),
            'user': orm.relationship(User, backref=orm.backref('quotes'))})
    orm.mapper(QuoteVote, t_quote_votes, properties={
            'quote': orm.relationship(Quote, backref='votes'),
            'user': orm.relationship(User, backref='quote_votes')})
    orm.mapper(Topic, t_topics)
    orm.mapper(User, t_users, properties={
            'topics': orm.relationship(Topic, backref='user')})


class Info(object):

    pass


class User(object):

    def posts_per_dow(self, start_date=None, end_date=None):
        q = select([func.date_part('isodow', t_posts.c.created_at),
                    func.count(t_posts.c.id)]). \
                    where(and_(t_posts.c.user_id==self.id,
                               t_posts.c.created_at>=start_date,
                               t_posts.c.created_at<end_date)). \
                    group_by('1'). \
                    order_by('1')

        data = dict(meta.Session.execute(q).fetchall())
        days = dict([(day, 0) for day in range(1, 8)])
        return dict(days, **data).values()

    def posts_per_hour(self, start_date=None, end_date=None):
        q = select([func.date_part('hour', t_posts.c.created_at),
                    func.count(t_posts.c.id)]). \
                    where(and_(t_posts.c.user_id==self.id,
                               t_posts.c.created_at>=start_date,
                               t_posts.c.created_at<end_date)). \
                               group_by('1'). \
                               order_by('1')

        data = dict(meta.Session.execute(q).fetchall())
        hours = dict([(hour, 0) for hour in range(0, 24)])
        return dict(hours, **data).values()


class Post(object):

    pass


class Quote(object):

    def __init__(self, post, user):
        self.created_at = datetime.datetime.now()
        self.post = post
        self.user = user

    def voted_by(self, user):
        return meta.Session.query(QuoteVote). \
            filter(QuoteVote.quote==self). \
            filter(QuoteVote.user==user). \
            count() != 0


class QuoteVote(object):

    def __init__(self, quote, user, is_upvote):
        self.created_at = datetime.datetime.now()
        self.quote = quote
        self.user = user
        self.upvoted = (is_upvote == True)


class Topic(object):

    def full_title(self):
        if self.subtitle:
            return ', '.join([self.title, self.subtitle])
        else:
            return self.title
