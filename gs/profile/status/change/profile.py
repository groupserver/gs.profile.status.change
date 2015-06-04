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
from gs.profile.base import ProfileViewlet as ProfileViewletBase
from gs.profile.image.base import get_file as get_image_file


class ProfileViewlet(ProfileViewletBase):
    'The viewlet for the Profile section'

    @Lazy
    def hasImage(self):
        try:
            retval = get_image_file(self.context, self.userInfo) is not None
        except IOError:
            retval = False
        assert(type(retval) == bool)
        return retval

    @Lazy
    def profileUrl(self):
        r = '{0}{1}'
        retval = r.format(self.siteInfo.url, self.userInfo.url)
        return retval

    @Lazy
    def profileImageUrl(self):
        r = '{0}/gs-profile-image-square/70'
        retval = r.format(self.profileUrl)
        return retval

    @Lazy
    def changeImageUrl(self):
        r = '{0}/image.html'
        retval = r.format(self.profileUrl)
        return retval

    @Lazy
    def biography(self):
        retval = self.userInfo.get_property('biography', '')
        retval = retval.strip() if retval else ''
        return retval

    @Lazy
    def changeProfileUrl(self):
        r = '{0}/edit.html'
        retval = r.format(self.profileUrl)
        return retval
