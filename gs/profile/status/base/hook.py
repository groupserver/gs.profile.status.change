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
from json import dumps as to_json
from logging import getLogger
log = getLogger('gs.profile.status.base.hook')
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from gs.content.form.api.json import SiteEndpoint
from gs.auth.token import log_auth_error
from .interfaces import (IGetPeople, ISendNotification)


class MembersHook(SiteEndpoint):
    '''The page that gets a list of people to send the status reminder to'''
    label = 'Get the people to send the digest to'
    form_fields = form.Fields(IGetPeople, render_context=False)

    @form.action(label='Get', name='get', prefix='',
                 failure='handle_get_people_failure')
    def handle_get_people(self, action, data):
        '''The form action for the *Get members* page.

:param action: The button that was clicked.
:param dict data: The form data.'''
        log.info('Getting the list of profile identifiers')
        retval = to_json(self.profile_ids)
        return retval

    def handle_get_people_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        retval = self.build_error_response(action, data, errors)
        return retval

    @Lazy
    def profile_ids(self):
        acl_users = self.context.acl_users
        retval = list(acl_users.objectIds('Custom User'))
        return retval


class SendNotification(SiteEndpoint):
    '''The page that sends a status-reminder to a person'''
    label = 'Send a status reminder'
    form_fields = form.Fields(ISendNotification, render_context=False)

    @form.action(label='Send', name='send', prefix='',
                 failure='handle_send_failure')
    def handle_send(self, action, data):
        '''The form action for the *Send notification* page.

:param action: The button that was clicked.
:param dict data: The form data.'''
        m = 'Sending the status notification to {0}'
        msg = m.format(data['profileId'])
        log.info(msg)
        retval = to_json(data)
        return retval

    def handle_send_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        retval = self.build_error_response(action, data, errors)
        return retval
