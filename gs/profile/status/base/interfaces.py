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
from __future__ import unicode_literals
from zope.interface import Interface
from zope.schema import ASCIILine
from zope.viewlet.interfaces import IViewletManager
from gs.auth.token import AuthToken


class IGetPeople(Interface):
    'Get the people'
    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)


class ISendNotification(Interface):
    '''Declares the form that will be used to send the notification.'''

    profileId = ASCIILine(
        title='Profile identifier',
        required=True)

    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)


class IProfileStatusNotification(IViewletManager):
    '''A viewlet manager for the profile status notification'''
