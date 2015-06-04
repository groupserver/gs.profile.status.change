# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
import sqlalchemy as sa  # lint:ok
from gs.database import getTable, getSession


class SkipQuery(object):
    def __init__(self):
        self.skipTable = getTable('profile_notification_skip')

    def skip_people(self):
        s = self.skipTable.select()

        session = getSession()
        r = session.execute(s)

        retval = [x['user_id'] for x in r]
        return retval

    def has_skip(self, userId):
        s = self.skipTable.select()
        s.append_whereclause(self.skipTable.c.user_id == userId)

        session = getSession()
        r = session.execute(s)

        retval = bool(r.rowcount)
        return retval

    def add_skip(self, userId):
        i = self.skipTable.insert()
        d = {'user_id': userId}

        session = getSession()
        session.execute(i, params=d)

    def remove_skip(self, userId):
        d = self.skipTable.delete(self.skipTable.c.user_id == userId)
        session = getSession()
        session.execute(d)
