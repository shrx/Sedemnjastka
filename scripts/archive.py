#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from optparse import OptionParser
import ConfigParser
import hashlib
import logging
import logging.config
import os.path
import random
import re
import urllib2
import warnings

import Image
import lxml.etree
import lxml.html
import mechanize
import pytz
import sqlalchemy as sa
from sqlalchemy import orm

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


parser = OptionParser()
parser.add_option("-f", "--full-force", action="store_true", dest="force",
                  help="force full archival run")

(options, args) = parser.parse_args()


browser = mechanize.Browser()
cj = mechanize.CookieJar()
cj.set_policy(MyCookiePolicy())
browser.set_cookiejar(cj)

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

AVATARS_DIR = os.path.join(os.path.dirname(__file__),
                           config.get('misc', 'avatars_dir'))
BASE_URL = config.get('forum', 'url').rstrip('/')

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), 'config.ini'))
logger = logging.getLogger(config.get('misc', 'logger'))

# Set up database
engine = sa.create_engine(config.get('database', 'url'))
engine.connect()
metadata = sa.MetaData(engine)
Session = orm.sessionmaker(bind=engine)
session = Session()

t_avatars = sa.Table('avatars', metadata, autoload=True)
t_info = sa.Table('info', metadata, autoload=True)
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    t_posts = sa.Table('posts', metadata, autoload=True)
t_topics = sa.Table('topics', metadata, autoload=True)
t_users = sa.Table('users', metadata, autoload=True)


class Avatar(object):

    __tablename__ = 'avatars'

    def __init__(self, md5sum, user):
        self.md5sum = md5sum
        self.user = user


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


orm.mapper(Avatar, t_avatars, properties={
        'user': orm. \
            relationship(User, uselist=False,
                         primaryjoin=t_avatars.c.user_id==t_users.c.id)})
orm.mapper(Info, t_info)
orm.mapper(Post, t_posts, properties={
        'avatar': orm.relationship(Avatar, uselist=False)})
orm.mapper(Topic, t_topics)
orm.mapper(User, t_users, properties={
        'avatar': orm. \
            relationship(Avatar, uselist=False,
                         primaryjoin=t_users.c.avatar_id==t_avatars.c.id,
                         post_update=True),
        'avatars': orm. \
            relationship(Avatar,
                         primaryjoin=t_avatars.c.user_id==t_users.c.id)})


# Set up the scrapers
def scrape_uid(tree):
    try:
        return re.findall('showuser=([0-9]+)',
                          tree.xpath('../..//td[@class="row1"]/a/@href')[0])[0]
    except IndexError:
        return 0 # Izbrisani

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
    if not tree.xpath('../../..//span[@class="unreg"]'):
        href = tree.xpath('../../..//span[@class="normalname"]/a/@href')[0]
        return re.findall('showuser=([0-9]+)', href)[0]
    else:
        return 0 # Izbrisani

def scrape_nick_name(tree):
    try:
        return tree.xpath('../../..//span[@class="unreg"]/text()')[0][10:-2]
    except IndexError:
        try:
            return tree. \
                xpath('../../..//div[@class="popupmenu-item"]/strong/text()')[0]
        except IndexError:
            return tree.xpath('../../..//span[@class="normalname"]/a/text()')[0]

topic_s = Scraper({
        'next_page': u'//a[@title="Sledeča stran"]/@href',
        'posts[]'  : ('//div[@class="postcolor"]', Scraper({
                    'avatar'    : '../..//span[@class="postdetails"]' + \
                        '/img[contains(@src, "//av")]/@src',
                    'body'      : scrape_body,
                    'created_at': scrape_created_at,
                    'nick_name' : scrape_nick_name,
                    'user_id'   : scrape_user_id,
                    })),
        })


profile_s = Scraper({
        'nick_name': '//h3/text()',
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
            data = profile_s.scrape(tree)
            user = User(topic.user_id, data['nick_name'])
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
                if post['user_id']:
                    user = session.query(User).get(post['user_id'])
                    if not user:
                        browser.open('%s/?showuser=%s' % (BASE_URL,
                                                          post['user_id']))
                        tree = lxml.html.parse(browser.response())
                        d2 = profile_s.scrape(tree)
                        user = User(post['user_id'], d2['nick_name'])
                        session.add(user)
                        session.commit()
                else:
                    user = session.query(User). \
                        filter(User.nick_name==post['nick_name']).first()
                    if not user:
                        user = session.query(User).get(0)

                new_post = Post(post['body'], post['created_at'],
                                topic.id, user.id)

                # Avatar
                if post['avatar']:
                    req = mechanize.Request(post['avatar'])
                    if user.avatar:
                        http_date = '%a, %d %b %Y %H:%M:%S GMT'
                        req.add_header('If-Modified-Since',
                                       user.avatar.created_at. \
                                           astimezone(pytz.utc). \
                                           strftime(http_date))
                    try:
                        browser.open(req)
                        md5sum = hashlib. \
                            md5(browser.response().read()).hexdigest()
                        if not user.avatar or md5sum != user.avatar.md5sum:
                            logger. \
                                info('Fetching *NEW AVATAR* for user "%s"' % \
                                         user.nick_name)
                            img = Image.open(browser.response())
                            if img.format == 'GIF': ext = '.gif'
                            elif img.format == 'JPEG': ext = '.jpg'
                            elif img.format == 'PNG': ext = '.png'

                            av = Avatar(md5sum, user)
                            session.add(av)
                            user.avatar = av
                            session.commit()
                            new_post.avatar = av

                            path = os.path.join(AVATARS_DIR,
                                                '%d%s' % (av.id, ext))
                            with open(path, 'wb') as f:
                                f.write(browser.response().read())

                            av.filename = os.path.basename(path)
                            av.width, av.height = img.size

                            # Create 48x48 thumbnail for archive's fancy view
                            av.thumb_filename = '%d_thumb%s' % (av.id, ext)
                            img.thumbnail((48, 48), Image.ANTIALIAS)
                            thumb_path = os.path.join(AVATARS_DIR,
                                                      av.thumb_filename)
                            if 'transparency' in img.info:
                                img.save(thumb_path,
                                         transparency=img.info['transparency'])
                            else:
                                img.save(thumb_path)
                            av.thumb_width, av.thumb_height = img.size
                        else:
                            new_post.avatar = user.avatar
                    except urllib2.HTTPError, e:
                        # 304 - Not Modified
                        if e.code == 304: new_post.avatar = user.avatar
                        elif e.code == 404: pass
                        else: raise
                else:
                    user.avatar = None

                session.add(new_post)
                topic.last_post_created_at = new_post.created_at
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
        next_page = '%s/?act=SF&f=17' % BASE_URL
        while next_page:
            browser.open(next_page)
            data = forum_s.scrape(lxml.html.parse(browser.response()))

            for topic in data['topics[]']:
                next_page = data['next_page']
                ot = session.query(Topic).get(topic['id'])
                # if this is an old topic in need of update
                if ot and ot.num_of_posts < int(topic['odgovori']) + 1:
                    logger.info('Archiving *OLD* topic #%s.' % ot.id)
                    self.archive.archive(ot)
                # if this is a new topic
                elif not ot:
                    nt = Topic(topic['id'], topic['title'],
                               topic['subtitle'], topic['user_id'])
                    logger.info('Archiving *NEW* topic #%s.' % nt.id)
                    self.archive.archive(nt)
                # else it is an already up-to-date topic, so we're done
                # unless full force is in effect
                elif not options.force:
                    next_page = None


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
    alr.value = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'do-not-run')):
        pass
    else:
        main()
