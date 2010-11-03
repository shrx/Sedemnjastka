#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import ConfigParser
import logging
import logging.config
import random
import re
import os.path

import lxml.etree
import lxml.html
import mechanize
import sqlalchemy
import sqlalchemy.orm

from scraper import Scraper


class MyCookiePolicy(mechanize.DefaultCookiePolicy):

    def set_ok(self, cookie, request):
        if not mechanize.DefaultCookiePolicy.set_ok(self, cookie, request):
            return False
        # This is a bad cookie.
        # IPB just seems to append to it the topics we've read, until it
        # overflows the platform specific limit on header field sizes.
        if cookie.name == 'mn3njalnik_topicsread':
            return False
        return True


browser = mechanize.Browser()
cj = mechanize.CookieJar()
cj.set_policy(MyCookiePolicy())
browser.set_cookiejar(cj)

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

BASE_URL = config.get('forum', 'url').rstrip('/')

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'config.ini'))
logger = logging.getLogger(config.get('misc', 'logger'))

# Set up database
engine = sqlalchemy.create_engine(config.get('database', 'url'))
engine.connect()
metadata = sqlalchemy.MetaData(engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

info_table = sqlalchemy.Table('info', metadata, autoload=True)
posts_table = sqlalchemy.Table('posts', metadata, autoload=True)
topics_table = sqlalchemy.Table('topics', metadata, autoload=True)
users_table = sqlalchemy.Table('users', metadata, autoload=True)


class Info(object):

    __tablename__ = 'info'


class Post(object):

    __tablename__ = 'posts'

    def __init__(self, body, created_at, topic_id, user_id):
        self.body = body
        self.created_at = created_at
        self.topic_id = topic_id
        self.user_id = user_id


class Topic(object):

    __tablename__ = 'topics'

    def __init__(self, id, title, subtitle, user_id):
        self.id = id and int(id)
        self.title = title and unicode(title)
        self.subtitle = subtitle and unicode(subtitle)
        self.user_id = user_id and int(user_id)


class User(object):

    __tablename__ = 'users'

    def __init__(self, id, nick_name):
        self.id = id and int(id)
        self.nick_name = nick_name and unicode(nick_name)


sqlalchemy.orm.mapper(Info, info_table)
sqlalchemy.orm.mapper(Post, posts_table)
sqlalchemy.orm.mapper(Topic, topics_table)
sqlalchemy.orm.mapper(User, users_table)

# Set up the scrapers
def scrape_uid(tree):
    return re.findall('showuser=([0-9]+)',
                      tree.xpath('../..//td[@class="row1"]/a/@href')[0])[0]

forum_s = Scraper({
        'next_page' : u'//a[@title="Sledeča stran"]/@href',
        'topics[]'  : ('//a[contains(@href, "who_posted")]', Scraper({
                    'id'       : lambda t: t.attrib['href'][22:-2],
                    'odgovori' : lambda t: int(''.join(t.text.split('.'))),
                    'subtitle' : '../..//div[@class="desc"]/text()',
                    'title'    : '../..//a[contains(@title, "Ta tema")]/text()',
                    'user_id'  : scrape_uid,
                    })),
        })

def scrape_created_at(tree):
    today = tree.xpath('//table[@id="gfooter"]//td/text()')[-1].split(' ')[3]
    created_at = tree.xpath('../../..//span[@class="postdetails"]')[0]. \
        text_content().strip()

    # Parse
    fmt = config.get('misc', 'datetime_format')
    if created_at.startswith('danes'):
        return datetime.strptime(created_at.replace('danes', today), fmt)
    elif created_at.startswith(u'včeraj'):
        return datetime.strptime(created_at.replace(u'včeraj', today),
                                 fmt) - timedelta(days=1)
    else:
        return datetime.strptime(created_at, fmt)

def scrape_body(tree):
    body = lxml.etree.tostring(tree, encoding=unicode)
    return body[23:body.rindex('</div>')]

def scrape_user_id(tree):
    href = tree.xpath('../../..//span[@class="normalname"]/a/@href')[0]
    return re.findall('showuser=([0-9]+)', href)[0]

def scrape_nick_name(tree):
    try:
        return tree.xpath('../../..//div[@class="popupmenu-item"]/' +
                          'strong/text()')[0]
    except IndexError:
        return tree.xpath('../../..//span[@class="normalname"]/a/text()')[0]

topic_s = Scraper({
        'next_page': u'//a[@title="Sledeča stran"]/@href',
        'posts[]'  : ('//div[@class="postcolor"]', Scraper({
                    'body'      : scrape_body,
                    'created_at': scrape_created_at,
                    'nick_name' : scrape_nick_name,
                    'user_id'   : scrape_user_id,
                    })),
        })


class Error(Exception):
    pass


class LoginError(Error):
    pass


class UnknownItemError(Error):
    pass


class Archive:

    def archive(self, item):
        if type(item) == Topic:
            self.archive_topic(item)
        else:
            raise UnknownItemError

    def archive_topic(self, topic):
        user = session.query(User).get(topic.user_id)
        if not user:
            browser.open('%s/?showuser=%s' % (BASE_URL, topic.user_id))
            tree = lxml.html.parse(browser.response())
            user = User(topic.user_id, tree.xpath('//h3/text()')[0])
            session.add(user)
            session.commit()

        ot = session.query(Topic).get(topic.id)
        if ot:
            topic = ot
        else:
            session.add(topic)
            user.num_of_topics = User.num_of_topics + 1
            session.commit()

        # Now do the posts
        st = (topic.num_of_posts / 40) * 40
        browser.open('%s/?showtopic=%s&st=%s' % (BASE_URL, topic.id, st))
        data = topic_s.scrape(lxml.html.parse(browser.response()))
        offset = topic.num_of_posts - st
        data['posts[]'] = data['posts[]'][offset:]

        while True:
            for post in data['posts[]']:
                user = session.query(User).get(post['user_id'])
                if not user:
                    user = User(post['user_id'], post['nick_name'])
                    session.add(user)
                    session.commit()

                post = Post(post['body'], post['created_at'], topic.id, user.id)
                session.add(post)
                topic.last_post_created_at = post.created_at
                topic.num_of_posts = Topic.num_of_posts + 1
                user.num_of_posts = User.num_of_posts + 1
                session.commit()

            # Go to next page
            if data['next_page'] is not None:
                browser.open(data['next_page'])
                data = topic_s.scrape(lxml.html.parse(browser.response()))
            else:
                break


class Crawler:

    def __init__(self):
        self.archive = Archive()

    def crawl(self):
        browser.open('%s/?act=SF&f=17' % BASE_URL)
        data = forum_s.scrape(lxml.html.parse(browser.response()))

        while True:
            for topic in data['topics[]']:
                ot = session.query(Topic).get(topic['id'])
                if ot and ot.num_of_posts < int(topic['odgovori']) + 1:
                    logger.info('Archiving *OLD* topic #%s.' % ot.id)
                    self.archive.archive(ot)
                elif not ot:
                    nt = Topic(topic['id'], topic['title'],
                               topic['subtitle'], topic['user_id'])
                    logger.info('Archiving *NEW* topic #%s.' % nt.id)
                    self.archive.archive(nt)

            if data['next_page'] is not None:
                browser.open(data['next_page'])
                data = forum_s.scrape(lxml.html.parse(browser.response()))
            else:
                break


def login(username, password):
    browser.open('%s/?act=Login&CODE=00' % BASE_URL)
    browser.select_form(name='LOGIN')
    browser.form['UserName'] = username
    browser.form['PassWord'] = password
    browser.submit()

    browser.open(BASE_URL)
    data = browser.response().read()
    if 'Prijavljen si' not in data or 'Latrina mnenjalnika' not in data:
        raise LoginError


def update_info():
    alr = session.query(Info).filter(Info.attribute=='archive_last_run').first()
    alr.value = datetime.now().strftime(config.get('misc', 'datetime_format'))
    session.commit()


def main():
    update_info()

    login(config.get('forum', 'username'), config.get('forum', 'password'))

    greetings = config.get('misc', 'greetings').split(', ')
    greeting = greetings[random.randrange(len(greetings))]

    logger.info("%s, I'm logged into the net!" % greeting)

    Crawler().crawl()

    partings = config.get('misc', 'partings').split(', ')
    parting = partings[random.randrange(len(partings))]

    logger.info('%s, I am done.' % parting)


if __name__ == '__main__':
    main()
