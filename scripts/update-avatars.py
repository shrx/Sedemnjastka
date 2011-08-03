#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime
import os
import os.path
import sys
import time
import urllib2

import lxml.html
import mechanize
import pytz
import sqlalchemy
import sqlalchemy.orm

from scraper import Scraper

AVATAR_DIR = None

browser = mechanize.Browser()

config = ConfigParser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

BASE_URL = config.get('forum', 'url').rstrip('/')

engine = sqlalchemy.create_engine(config.get('database', 'url'))
engine.connect()
metadata = sqlalchemy.MetaData(engine)
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

users_table = sqlalchemy.Table('users', metadata, autoload=True)

profile_s = Scraper({
        'avatar': '//div[@class="pp-name"]//img[contains(@src, "//av")]/@src',
        })


class HeadRequest(mechanize.Request):

    def get_method(self):
        return 'HEAD'


class User(object):

    __tablename__ = 'users'

    def update_avatar(self):
        url = None
        if self.avatar:
            req = HeadRequest('%s/uploads//%s' % \
                                  (BASE_URL, os.path.basename(self.avatar)))
            req.add_header('If-Modified-Since', \
                               self.avatar_last_updated. \
                               astimezone(pytz.utc). \
                               strftime('%a, %d %b %Y %H:%M:%S GMT'))
            try:
                browser.open(req)
                url = req.get_full_url()
            except urllib2.HTTPError, e:
                # 304 - Not Modified
                if e.code == 304: return
                elif e.code == 404: pass
                # re-
                else: raise

        # Remove old avatar
        if self.avatar:
            path = os.path.join(AVATAR_DIR, os.path.basename(self.avatar))
            os.remove(path)
            self.avatar = None

        if not url:
            resp = browser.open('%s/?showuser=%s' % (BASE_URL, self.id))
            url = profile_s.scrape(lxml.html.parse(resp))['avatar']

        # Don't do nothing more if the user hasn't an avatar
        if url != None:
            # There is corruption in their database, requiring this
            try:
                resp = browser.open(url)
                path = os.path.join(AVATAR_DIR, os.path.basename(url))
                with open(path, 'wb') as f:
                    f.write(resp.read())
                    self.avatar = '%s' % os.path.basename(url)
            except urllib2.HTTPError:
                pass

        self.avatar_last_updated = pytz.utc.localize(datetime.datetime.utcnow())


sqlalchemy.orm.mapper(User, users_table)


def main():
    for user in session.query(User):
        user.update_avatar()
        session.add(user)
        session.commit()


def usage():
    print >> sys.stderr, "Usage: update-avatars.py AVATAR_DIRECTORY"


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage()
    else:
        AVATAR_DIR = sys.argv[1]
        main()
