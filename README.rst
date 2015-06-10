============================
``gs.profile.status.change``
============================
------------------------------------------------
Toggle receiving the profile-status notification
------------------------------------------------

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2015-06-10
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

This product provides the `email command`_ and page_ that either
stop or enables *Profile status* notification (*What is going on
in your groups*) from going out.

Email command
=============

The email command [#command]_ ``Summary off`` is registered for
the support-groups. It adds the user-identifier for the sender to
the ``summary_skip`` table.

Page
====

The page ``notification.html``, in the *profile* context,
provides a toggle to turn the monthly status notification on or
off. The name of the page is quite generic, with the idea that it
will be possible to configure different notification settings.

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.profile.status.change
- Translations:
  https://www.transifex.com/projects/p/gs-profile-status-change/
- Questions and comments to
  http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver
    
.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

.. [#command] See
              <https://github.com/groupserver/gs.group.list.command>

..  LocalWords:  nz GSProfile TODO redirector LocalWords viewlets
