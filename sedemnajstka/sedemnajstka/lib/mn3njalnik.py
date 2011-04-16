# -*- coding: utf-8 -*-

import mechanize

class Error(Exception): pass

class LoginError(Error): pass

class PMError(Error): pass


class Mn3njalnik:

    BASE_URL = 'http://www.joker.si/mn3njalnik'

    def __init__(self):
        self.b = mechanize.Browser()

    def login(self, username, password):
        self.b.open('%s/?act=Login&CODE=00' % self.BASE_URL)
        self.b.select_form(name='LOGIN')
        self.b.form['UserName'] = username
        self.b.form['PassWord'] = password
        self.b.submit()

        self.b.open(self.BASE_URL)
        data = self.b.response().read()
        if 'Prijavljen si' not in data or 'Latrina mnenjalnika' not in data:
            raise LoginError

    def pm(self, to, subject, message):
        self.b.open('%s/?act=Msg&CODE=04' % self.BASE_URL)
        self.b.select_form(name='REPLIER')
        self.b.form['entered_name'] = to
        self.b.form['msg_title'] = subject
        self.b.form['Post'] = message
        self.b.submit()

        data = self.b.response().read()
        # Will receive redirect on success
        if not data.startswith('<script>location.href'):
            raise PMError
