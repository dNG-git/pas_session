# -*- coding: utf-8 -*-

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;session

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasSessionVersion)#
#echo(__FILEPATH__)#
"""

class AbstractAdapter(object):
    """
A session protocol adapter implements methods that rely on protocol specific
functionality.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self, session):
        """
Constructor __init__(AbstractAdapter)

:param session: Session instance

:since: v0.2.00
        """

        self.session = session
        """
Session instance
        """
    #

    def is_persistent(self):
        """
Returns true if the uuID session is set persistently at the client.

:return: (bool) True if set
:since:  v0.2.00
        """

        return False
    #

    def is_valid(self):
        """
Returns true if the defined session is valid.

:return: (bool) True if session is valid
:since:  v0.2.00
        """

        return True
    #

    def load(self):
        """
Uses protocol specific functionality to load additional information of an
session.

:since: v0.2.00
        """

        pass
    #

    def save(self):
        """
Uses protocol specific functionality to save additional information of an
session.

:since: v0.2.00
        """

        pass
    #

    @staticmethod
    def get_uuid():
        """
Returns the uuID.

:return: (str) Unique user identification; None if unknown
:since:  v0.2.00
        """

        return None
    #
#
