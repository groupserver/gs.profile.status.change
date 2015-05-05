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
from collections import namedtuple
from datetime import date
from functools import reduce
from operator import concat, attrgetter
from random import shuffle
import sys
if sys.version_info >= (3, ):  # pragma: no cover
    from urllib.parse import quote
else:  # Python 2
    from urllib import quote
from zope.app.pagetemplate import ViewPageTemplateFile
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.contentprovider.interfaces import UpdateNotCalled
from gs.core import curr_time, comma_comma_and
from gs.group.member.base import user_member_of_group, user_admin_of_group
from gs.group.privacy.interfaces import IGSGroupVisibility
from gs.group.stats import GroupPostingStats
from gs.profile.base import ProfileViewlet, ProfileContentProvider
from gs.site.member.sitemembershipvocabulary import SiteMembership
from gs.group.member.canpost.interfaces import IGSPostingUser
from Products.GSGroup.interfaces import IGSMailingListInfo
from Products.GSGroupMember.groupMembersInfo import GSGroupMembersInfo
from .queries import PostingStatsQuery

SiteGroups = namedtuple('SiteGroups', ['siteInfo', 'groupInfos'])


class GroupsViewlet(ProfileViewlet):
    'The groups viewlet'

    @Lazy
    def userGroups(self):
        self.userInfo.user.get

    @staticmethod
    def get_groupInfo(folder):
        retval = createObject('groupserver.GroupInfo', folder)
        return retval

    @staticmethod
    def get_siteInfo(folder):
        retval = createObject('groupserver.SiteInfo', folder)
        return retval

    def get_sitegroups(self, siteId):
        content = self.context.Content
        site = getattr(content, siteId)
        groups = getattr(site, 'groups')

        groupInfos = []
        for folder in groups.objectValues(['Folder', 'Folder (ordered)']):
            if user_member_of_group(self.userInfo, folder):
                groupInfo = self.get_groupInfo(folder)
                groupInfos.append(groupInfo)

        if groupInfos is []:
            m = 'Not a member of any groups in {0}'.format(siteId)
            raise ValueError(m)
        groupInfos.sort(key=attrgetter('name'))
        siteInfo = self.get_siteInfo(site)
        retval = SiteGroups(siteInfo=siteInfo, groupInfos=groupInfos)
        return retval

    @Lazy
    def sites(self):
        sites = list(SiteMembership(self.context))
        sites.sort(key=attrgetter('title'))
        retval = [self.get_sitegroups(s.token) for s in sites]

        return retval

    @Lazy
    def groups(self):
        retval = reduce(concat, [s.groupInfos for s in self.sites], [])
        return retval


class SiteInfo(ProfileContentProvider):
    'Ths site-information content provider'
    def __init__(self, profile, request, view):
        super(SiteInfo, self).__init__(profile, request, view)
        self.__updated = False

    @Lazy
    def isAdmin(self):
        site = self.siteInfo.siteObj
        user = self.userInfo.user
        retval = ('DivisionAdmin' in user.getRolesInContext(site))
        assert type(retval) == bool
        return retval

    def update(self):
        self.__updated = True

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        r = pageTemplate(self)
        return r


class GroupInfo(ProfileContentProvider):
    'Ths group-information content provider'
    def __init__(self, profile, request, view):
        super(GroupInfo, self).__init__(profile, request, view)
        self.__updated = False

    def update(self):
        self.__updated = True

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
        pageTemplate = ViewPageTemplateFile(self.pageTemplateFileName)
        r = pageTemplate(self)
        return r

    # Methods and properties that are not part of the standard content
    # provider API are below this point

    @Lazy
    def isAdmin(self):
        '''Is the user an administrator of the group?

:returns: ``True`` if the user is a group administrator.
:rtype: bool'''
        retval = user_admin_of_group(self.userInfo, self.groupInfo)
        return retval

    @Lazy
    def groupVisibility(self):
        retval = IGSGroupVisibility(self.groupInfo)
        return retval

    @Lazy
    def groupStats(self):
        retval = GroupPostingStats(self.groupInfo)
        return retval

    @Lazy
    def membersInfo(self):
        retval = GSGroupMembersInfo(self.groupInfo.groupObj)
        return retval

    @Lazy
    def privacyTooStrict(self):
        '''Is the privacy of the group too tight?

:returns: ``True`` if the user is a group administrator, the privacy
          of the group is ``secret``, and there are more than a dozen
          members.
:rtype: bool'''
        retval = (self.isAdmin and self.groupVisibility.isSecret
                  and (self.membersInfo.fullMemberCount > 12))
        return retval

    @Lazy
    def statsQuery(self):
        retval = PostingStatsQuery()
        return retval

    @Lazy
    def previousMonth(self):
        '''Get the previous month from now

:returns: The previous month.
:rtype: datetime.date'''
        dt = curr_time()
        if dt.month == 1:
            newMonth = 12
            newYear = dt.year - 1
        else:
            newMonth = dt.month - 1
            newYear = dt.year
        retval = date(newYear, newMonth, 1)
        return retval

    @Lazy
    def nPosts(self):
        'The number of posts the previous month'
        pm = self.previousMonth
        retval = self.statsQuery.posts_in_month(
            pm.month, pm.year, self.groupInfo.id, self.siteInfo.id)
        return retval

    @Lazy
    def authorIds(self):
        pm = self.previousMonth
        retval = self.statsQuery.authors_in_month(
            pm.month, pm.year, self.groupInfo.id, self.siteInfo.id)
        shuffle(retval)  # Mostly for self.people
        return retval

    @Lazy
    def nAuthors(self):
        'The number of authors in the previous month'
        retval = len(self.authorIds)
        return retval

    @Lazy
    def people(self):
        '''Five random recent authors, not including this person

:returns: The names of five recent authors, seperated by commas
:rtype: str'''
        # Get five authors, because we are going to throw one away.
        authorIds = self.authorIds[:6]
        # Throw an author away.
        try:
            authorIds.remove(self.userInfo.id)
        except ValueError:
            authorIds = authorIds[:5]  # User not in the list. No worries.
        authorNames = [createObject('groupserver.UserFromId',
                                    self.groupInfo.groupObj, uId).name
                       for uId in authorIds]
        retval = comma_comma_and(authorNames)
        if self.nAuthors != len(authorNames):
            retval = 'including {0}'.format(retval)
        return retval

    @Lazy
    def nTopics(self):
        pm = self.previousMonth
        retval = self.statsQuery.topics_in_month(
            pm.month, pm.year, self.groupInfo.id, self.siteInfo.id)
        return retval

    @Lazy
    def canPost(self):
        retval = IGSPostingUser(self.userInfo, self.groupInfo).canPost
        return retval

    @Lazy
    def groupEmail(self):
        l = IGSMailingListInfo(self.groupInfo.groupObj)
        retval = l.get_property('mailto')
        return retval

    @Lazy
    def unsubscribeLink(self):
        to = quote(self.groupEmail)
        subject = quote('Unsubscribe')
        b = '''Hello,

Please remove me from {0}
<{1}>.

--
{2} <{3}{4}>'''
        body = quote(b.format(self.groupInfo.name, self.groupInfo.url,
                              self.userInfo.name,
                              self.siteInfo.url, self.userInfo.url))
        mailto = 'mailto:{to}?Subject={subject}&body={body}'
        retval = mailto.format(to=to, subject=subject, body=body)
        return retval