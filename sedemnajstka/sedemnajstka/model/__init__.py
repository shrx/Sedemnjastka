"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from sedemnajstka.model import meta


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.Base.metadata.bind = engine

    t_info = sa.Table('info', meta.Base.metadata, autoload=True)
    t_posts = sa.Table('posts', meta.Base.metadata, autoload=True)
    t_topics = sa.Table('topics', meta.Base.metadata, autoload=True)
    t_users = sa.Table('users', meta.Base.metadata, autoload=True)

    orm.mapper(Info, t_info)
    orm.mapper(Post, t_posts)
    orm.mapper(Topic, t_topics)
    orm.mapper(User, t_users, properties={
            'topics': orm.relationship(Topic, backref='user')})


class Info(object):
    pass


class User(object):
    pass


class Post(object):
    pass


class Topic(object):

    def full_title(self):
        if self.subtitle:
            return ', '.join([self.title, self.subtitle])
        else:
            return self.title
