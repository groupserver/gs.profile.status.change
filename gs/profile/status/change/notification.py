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
from gs.content.email.base import SiteEmail, TextMixin


class ProfileStatus(SiteEmail):
    'The profile-status notification'


class ProfileStatusText(ProfileStatus, TextMixin):
    def __init__(self, profile, request):
        super(ProfileStatusText, self).__init__(profile, request)
        f = 'gs-profile-status-{0}.txt'
        filename = f.format(profile.getId())
        self.set_header(filename)
