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
from zope.cachedescriptors.property import Lazy
from gs.profile.base import ProfileViewlet
from .utils import mailto


class SupportViewlet(ProfileViewlet):
    'The viewlet for the Support section'

    @Lazy
    def supportEmail(self):
        retval = self.siteInfo.get_support_email()
        return retval

    @Lazy
    def helpEmailAddress(self):
        b = '''Hello,

I received the monthly summary of what is going on in my groups and...

--
Me: <{0}{1}>
'''
        body = b.format(self.siteInfo.url, self.userInfo.url)
        retval = mailto(self.supportEmail, 'Monthly status notification',
                        body)
        return retval

    @Lazy
    def stopEmailAddress(self):
        b = '''Hello,

Please stop sending me the monthly summary of what is going on in my groups.

--
Me: <{0}{1}>
'''
        body = b.format(self.siteInfo.url, self.userInfo.url)
        retval = mailto(self.supportEmail, 'Summary off', body)
        return retval
