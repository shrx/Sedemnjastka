#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os.path
import sys
import urllib2

import lxml.html
import mechanize
import sqlalchemy
import sqlalchemy.orm

from scraper import Scraper

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
        if self.avatar:
            req = HeadRequest(self.avatar)
            try:
                browser.open(req)
                return
            except urllib2.HTTPError, e:
                if e.code == 404: pass
                # re-
                else: raise

        resp = browser.open('%s/?showuser=%s' % (BASE_URL, self.id))
        self.avatar = profile_s.scrape(lxml.html.parse(resp))['avatar']


sqlalchemy.orm.mapper(User, users_table)


def main():
    count = session.query(User).count()
    for i, user in enumerate(session.query(User)):
        user.update_avatar()
        session.add(user)
        session.commit()
        print 'DONE - %s/%s' % (i, count)


if __name__ == '__main__':
    main()
