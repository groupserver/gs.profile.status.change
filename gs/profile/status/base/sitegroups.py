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
from __future__ import absolute_import, print_function, unicode_literals
from operator import attrgetter
from zope.component import createObject
from gs.group.member.base import user_member_of_group


class NoGroups(ValueError):
    'No groups on the site'


class SiteGroups(object):
    def __init__(self, user, site):
        groups = getattr(site, 'groups')
        self.groupInfos = []
        for folder in groups.objectValues(['Folder', 'Folder (ordered)']):
            if user_member_of_group(user, folder):
                groupInfo = self.get_groupInfo(folder)
                self.groupInfos.append(groupInfo)
        if self.groupInfos is []:
            m = 'Not a member of any groups in {0}'.format(site.getId())
            raise NoGroups(m)
        self.groupInfos.sort(key=attrgetter('name'))

        self.siteInfo = self.get_siteInfo(site)

    @staticmethod
    def get_groupInfo(folder):
        retval = createObject('groupserver.GroupInfo', folder)
        return retval

    @staticmethod
    def get_siteInfo(folder):
        retval = createObject('groupserver.SiteInfo', folder)
        return retval
