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
import sys
if sys.version_info >= (3, ):  # pragma: no cover
    from urllib.parse import quote
else:  # Python 2
    from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.profile.base import ProfileViewlet


class SupportViewlet(ProfileViewlet):
    'The viewlet for the Support section'

    mailto = 'mailto:{to}?Subject={subject}&body={body}'

    @Lazy
    def supportEmail(self):
        retval = self.siteInfo.get_support_email()
        return retval

    @Lazy
    def helpEmailAddress(self):
        subject = quote('Monthly status notification')
        b = '''Hello,

I received the monthly summary of what is going on in my groups and...

--
Me: <{0}{1}>
'''
        body = quote(b.format(self.siteInfo.url, self.userInfo.url))
        retval = self.mailto.format(to=self.supportEmail, subject=subject,
                                    body=body)
        return retval

    @Lazy
    def stopEmailAddress(self):

        subject = quote('Summary off')
        b = '''Hello,

Please stop sending me the monthly summary of what is going on in my groups.

--
Me: <{0}{1}>
'''
        body = quote(b.format(self.siteInfo.url, self.userInfo.url))
        retval = self.mailto.format(to=self.supportEmail, subject=subject,
                                    body=body)
        return retval
