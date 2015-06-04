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
from __future__ import absolute_import, unicode_literals
from mock import patch
from unittest import TestCase
from gs.profile.status.base.command import StatusCommand
from gs.group.list.command.result import CommandResult
from .faux import (FauxGroupInfo, FauxUserInfo, faux_on_email,
                   faux_off_email)


class StatusOnTest(TestCase):

    def setUp(self):
        self.fauxGroup = FauxGroupInfo()

    @patch.object(StatusCommand, 'get_user')
    @patch('gs.profile.status.base.command.SkipQuery', autospec=True)
    def test_on(self, FauxSkipQuery, faux_get_user):
        faux_get_user.return_value = FauxUserInfo()
        c = StatusCommand(self.fauxGroup)
        e = faux_on_email()

        r = c.process(e, None)
        self.assertEqual(CommandResult.commandStop, r)
        FauxSkipQuery().remove_skip.assert_called_once_with(b'exampleuser')

    @patch.object(StatusCommand, 'get_user')
    @patch('gs.profile.status.base.command.SkipQuery', autospec=True)
    def test_on_nouser(self, FauxSkipQuery, faux_get_user):
        faux_get_user.return_value = None
        c = StatusCommand(self.fauxGroup)
        e = faux_on_email()

        r = c.process(e, None)
        self.assertEqual(CommandResult.commandContinue, r)
        self.assertEqual(0, FauxSkipQuery().remove_skip.call_count)


class StatusOffTest(TestCase):

    def setUp(self):
        self.fauxGroup = FauxGroupInfo()

    @patch.object(StatusCommand, 'get_user')
    @patch('gs.profile.status.base.command.SkipQuery', autospec=True)
    def test_off(self, FauxSkipQuery, faux_get_user):
        faux_get_user.return_value = FauxUserInfo()
        c = StatusCommand(self.fauxGroup)
        e = faux_off_email()

        r = c.process(e, None)
        self.assertEqual(CommandResult.commandStop, r)
        FauxSkipQuery().add_skip.assert_called_once_with(b'exampleuser')

    @patch.object(StatusCommand, 'get_user')
    @patch('gs.profile.status.base.command.SkipQuery', autospec=True)
    def test_off_nouser(self, FauxSkipQuery, faux_get_user):
        faux_get_user.return_value = None
        c = StatusCommand(self.fauxGroup)
        e = faux_off_email()

        r = c.process(e, None)
        self.assertEqual(CommandResult.commandContinue, r)
        self.assertEqual(0, FauxSkipQuery().remove_skip.call_count)
