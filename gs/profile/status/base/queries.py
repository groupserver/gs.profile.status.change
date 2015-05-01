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
import sqlalchemy as sa
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


class PostingStatsQuery(object):
    def __init__(self):
        self.postTable = getTable('post')
        self.topicTable = getTable('topic')

    def posts_in_month(self, month, year, groupId, siteId):
        'Get the number of posts in a particular month'
        pt = self.postTable
        s = sa.select([sa.func.count(pt.c.post_id).label('n_posts')])
        s.append_whereclause(sa.extract('month', pt.c.date) == month)
        s.append_whereclause(sa.extract('year', pt.c.date) == year)
        s.append_whereclause(pt.c.group_id == groupId)
        s.append_whereclause(pt.c.site_id == siteId)

        session = getSession()
        r = session.execute(s)

        retval = r.fetchone()['n_posts']
        return retval

    def topics_in_month(self, month, year, groupId, siteId):
        'Get the number of topics in a particular month'
        tt = self.topicTable
        s = sa.select([sa.func.count(tt.c.topic_id).label('n_topics')])
        s.append_whereclause(sa.extract('month', tt.c.last_post_date) == month)
        s.append_whereclause(sa.extract('year', tt.c.last_post_date) == year)
        s.append_whereclause(tt.c.group_id == groupId)
        s.append_whereclause(tt.c.site_id == siteId)

        session = getSession()
        r = session.execute(s)

        retval = r.fetchone()['n_topics']
        return retval
        return retval

    def authors_in_month(self, month, year, groupId, siteId):
        'Get the distinct user-ids of the authors in a particular month'
        pt = self.postTable
        s = sa.select([sa.func.distinct(pt.c.user_id).label('user_id')])
        s.append_whereclause(sa.extract('month', pt.c.date) == month)
        s.append_whereclause(sa.extract('year', pt.c.date) == year)
        s.append_whereclause(pt.c.group_id == groupId)
        s.append_whereclause(pt.c.site_id == siteId)

        session = getSession()
        r = session.execute(s)

        retval = [x['user_id'] for x in r]
        return retval
