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
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.profile.base import ProfileForm
from .interfaces import ToggleStatusCommand
from .queries import SkipQuery
from . import GSMessageFactory as _


class ChangeNotification(ProfileForm):
    label = _('change-notification', 'Change notification')
    pageTemplateFileName = 'browser/templates/page.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(ToggleStatusCommand, render_context=False)

    def __init__(self, context, request):
        super(ChangeNotification, self).__init__(context, request)

    @Lazy
    def query(self):
        retval = SkipQuery()
        return retval

    @property
    def skip(self):
        # Deliberately not lazy
        retval = self.query.has_skip(self.userInfo.id)
        return retval

    def setUpWidgets(self, ignore_request=False):
        data = {'skip': self.skip}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context,
            self.request, form=self, data=data,
            ignore_request=ignore_request)

    @form.action(name=b'change', label=_('change-button', 'Change'),
                 failure='handle_set_action_failure')
    def handle_change(self, action, data):
        if data['skip'] and not self.skip:
            self.query.add_skip(self.userInfo.id)
            self.status = _(
                'opt-out',
                'Opting out of the monthly profile-status notification.')
        elif not data['skip'] and self.skip:
            self.query.remove_skip(self.userInfo.id)
            self.status = _(
                'out-in',
                'Opting into the monthly profile-status notification.')
        else:
            # data['skip'] == self.skip
            if self.skip:
                self.status = _(
                    'no-change-skip',
                    'No change made: you are still skipping the '
                    'notification.')
            else:
                self.status = _(
                    'no-change-in',
                    'No change made: you are still receiving the '
                    'notification.')
            self.status = _('no-change', 'No change')

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            s = _('error-single', 'There is an error:')
        else:
            s = _('error-multiple', 'There are errors:')
        self.status = '<p>{0}</p>'.format(s)
