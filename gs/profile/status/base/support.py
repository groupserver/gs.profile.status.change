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

    @Lazy
    def emailAddress(self):
        mailto = 'mailto:{to}?Subject={subject}&body={body}'
        subject = quote('Monthly status notification')
        b = '''Hello,

I received the monthly status notification and...

--
Me: <{0}{1}>
'''
        body = quote(b.format(self.siteInfo.url, self.userInfo.url))
        retval = mailto.format(to=self.siteInfo.get_support_email(),
                               subject=subject, body=body)
        return retval
