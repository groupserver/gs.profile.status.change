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
from zope.interface import Interface
from zope.schema import Bool
from . import GSMessageFactory as _


class ToggleStatusCommand(Interface):
    skip = Bool(
        title=_('skip-label', 'Skip the monthly profile-status'),
        description=_('skip-help',
                      'Skip receiving the profile-status notification that '
                      'is sent out once a month'),
        default=False,
        required=True)
