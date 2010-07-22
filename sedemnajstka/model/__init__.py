"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

from sedemnajstka.model import meta


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.Base.metadata.bind = engine

    t_posts = sa.Table('posts', meta.Base.metadata, autoload=True)
    t_topics = sa.Table('topics', meta.Base.metadata, autoload=True)
    t_users = sa.Table('users', meta.Base.metadata, autoload=True)

    orm.mapper(Post, t_posts)
    orm.mapper(Topic, t_topics)
    orm.mapper(User, t_users)


class Post(object):
    __tablename__ = 'posts'


class Topic(object):
    __tablename__ = 'topics'


class User(object):
    __tablename__ = 'users'
