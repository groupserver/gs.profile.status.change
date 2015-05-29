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
from email.utils import parseaddr
from zope.cachedescriptors.property import Lazy
from gs.group.list.command import (CommandABC, CommandResult)
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .queries import SkipQuery


class StatusCommand(CommandABC):
    def __init__(self, supportGroup):
        self.group = self.supportGroup = supportGroup

    @Lazy
    def skipQuery(self):
        retval = SkipQuery()
        return retval

    def process(self, email, request):
        components = self.get_command_components(email)
        if components[0] != 'summary':
            m = 'Not a summary command: {0}'.format(email['Subject'])
            raise ValueError(m)

        retval = CommandResult.notACommand
        if (len(components) == 2):
            userInfo = self.get_user(email)
            if userInfo and (components[1] == 'on'):
                self.skipQuery.remove_skip(userInfo.id)
                retval = CommandResult.commandStop
            elif userInfo and (components[1] == 'off'):
                self.skipQuery.add_skip(userInfo.id)
                retval = CommandResult.commandStop
            elif not(userInfo):
                retval = CommandResult.commandContinue
        assert retval
        return retval

    @staticmethod
    def get_email_addr(emailMessage):
        retval = parseaddr(emailMessage['From'])[1]
        return retval

    def get_user(self, email):
        retval = None
        sr = self.group.site_root()
        addr = self.get_email_addr(email)
        user = sr.acl_users.get_userByEmail(addr)
        if user:
            retval = IGSUserInfo(user)
        return retval
