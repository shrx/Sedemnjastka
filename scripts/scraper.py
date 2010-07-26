#!/usr/bin/env python
# -*- coding: utf-8 -*-

import lxml.html


class Scraper(object):

    def __init__(self, items):
        self.items = items

    def scrape(self, tree):
        self.tree = tree

        data = {}
        for key, val in self.items.items():
            data[key] = self._get_value(val)
        return data

    def _get_value(self, val):
        if type(val) == tuple:
            xoc = val[0]
        else:
            xoc = val

        if callable(xoc):
            value = xoc(self.tree)
        else:
            if type(val) == tuple:
                value = self.tree.xpath(xoc)
            else:
                value = (self.tree.xpath(xoc) or [None])[0]

        if type(val) == tuple:
            data = []
            for i in value:
                data.append(val[1].scrape(i))
            return data
        else:
            return value
