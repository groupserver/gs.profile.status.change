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


class LoginQuery(object):

    def __init__(self):
        self.auditEventTable = getTable('audit_event')

    def user_has_login(self, userId):
        aet = self.auditEventTable

        s = aet.select()
        s.append_whereclause(aet.c.instance_user_id == userId)
        s.append_whereclause(aet.c.subsystem == 'groupserver.Login')
        s.append_whereclause(aet.c.event_code == '1')
        s.limit = 1

        session = getSession()
        r = session.execute(s)

        retval = bool(r.rowcount)
        return retval
