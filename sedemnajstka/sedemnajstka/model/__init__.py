"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.sql import select, func

from sedemnajstka.model import meta


t_info = None
t_posts = None
t_topics = None
t_users = None


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    meta.Session.configure(bind=engine)
    meta.Base.metadata.bind = engine

    global t_info, t_posts, t_topics, t_users
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

    def posts_per_dow(self):
        q = select([func.date_part('isodow', t_posts.c.created_at),
                    func.count(t_posts.c.id)]). \
                    where(t_posts.c.user_id==self.id). \
                    group_by('1'). \
                    order_by('1')
        data = dict(meta.Session.execute(q).fetchall())
        days = dict([(day, 0) for day in range(1, 8)])
        return dict(days, **data).values()

    def posts_per_hour(self):
        q = select([func.date_part('hour', t_posts.c.created_at),
                    func.count(t_posts.c.id)]). \
                    where(t_posts.c.user_id==self.id). \
                    group_by('1'). \
                    order_by('1')
        data = dict(meta.Session.execute(q).fetchall())
        hours = dict([(hour, 0) for hour in range(0, 24)])
        return dict(hours, **data).values()


class Post(object):

    pass


class Topic(object):

    def full_title(self):
        if self.subtitle:
            return ', '.join([self.title, self.subtitle])
        else:
            return self.title
