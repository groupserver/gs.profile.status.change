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
from gs.profile.email.base import EmailUser
from .queries import LoginQuery


class PasswordViewlet(ProfileViewlet):
    'The reset-password viewlet'

    @Lazy
    def query(self):
        retval = LoginQuery()
        return retval

    @Lazy
    def show(self):
        ''':returns: ``True`` if the member is yet to log in
:rtype: bool'''
        retval = not self.query.user_has_login(self.userInfo.id)
        assert(type(retval) == bool)
        return retval

    @Lazy
    def emailAddr(self):
        eu = EmailUser(self.context, self.userInfo)
        p = eu.get_delivery_addresses()
        v = eu.get_verified_addresses()
        u = eu.get_unverified_addresses()
        retval = p[0] if p else v[0] if v else u[0] if u else ''
        return retval

    @Lazy
    def passwordResetBaseURL(self):
        r = '{0}/reset_password.html'
        retval = r.format(self.siteInfo.url)
        return retval

    @Lazy
    def passwordResetUrl(self):
        r = '{0}?form.email={1}'
        retval = r.format(self.passwordResetBaseURL, quote(self.emailAddr))
        return retval
