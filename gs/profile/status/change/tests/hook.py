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
from mock import patch, MagicMock
from unittest import TestCase
from gs.profile.status.base.hook import MembersHook


class HookTest(TestCase):

    @patch('gs.profile.status.base.hook.SkipQuery', autospec=True)
    def test_profileIds_no_skip(self, FauxSkipQuery):
        FauxSkipQuery().skip_people.return_value = []
        context = MagicMock()
        expected = ['keep0', 'keep1', 'keep2']
        context.acl_users.getUserNames.return_value = expected

        mh = MembersHook(context, MagicMock())
        r = mh.profileIds

        self.assertEqual(r, expected)

    @patch('gs.profile.status.base.hook.SkipQuery', autospec=True)
    def test_profileIds_no_dupe(self, FauxSkipQuery):
        FauxSkipQuery().skip_people.return_value = []
        context = MagicMock()
        expected = ['keep0', 'keep1', 'keep2']
        returned = expected + ['keep1', ]
        context.acl_users.getUserNames.return_value = returned

        mh = MembersHook(context, MagicMock())
        r = mh.profileIds

        self.assertEqual(r, expected)

    @patch('gs.profile.status.base.hook.SkipQuery', autospec=True)
    def test_profileIds_skip(self, FauxSkipQuery):
        skip = ['skip0', 'skip1']
        FauxSkipQuery().skip_people.return_value = skip
        context = MagicMock()
        expected = ['keep0', 'keep1', 'keep2']
        returned = expected + skip
        context.acl_users.getUserNames.return_value = returned

        mh = MembersHook(context, MagicMock())
        r = mh.profileIds

        self.assertEqual(r, expected)
