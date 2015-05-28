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
from zope.component import getMultiAdapter
from gs.profile.notify import MessageSender
from Products.CustomUserFolder.interfaces import IGSUserInfo


class StatusNotifier(object):
    htmlTemplateName = 'gs-profile-status.html'
    textTemplateName = 'gs-profile-status.txt'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.htmlTemplateName)
        return retval

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.textTemplateName)
        return retval

    def notify(self):
        userInfo = IGSUserInfo(self.context)
        sender = MessageSender(self.context, userInfo)
        text = self.textTemplate()
        html = self.htmlTemplate()
        sender.send_message('What is happening in your groups', text, html)
