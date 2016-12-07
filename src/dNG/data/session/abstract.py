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

# pylint: disable=import-error, no-name-in-module

from dNG.controller.abstract_response import AbstractResponse
from dNG.data.logging.log_line import LogLine
from dNG.database.nothing_matched_exception import NothingMatchedException
from dNG.module.named_loader import NamedLoader
from dNG.runtime.not_implemented_exception import NotImplementedException
from dNG.runtime.type_exception import TypeException

from .abstract_adapter import AbstractAdapter

class Abstract(object):
    """
The "Abstract" class is used to provide a thread-safe interface for user
sessions.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    # pylint: disable=unused-argument

    def __init__(self):
        """
Constructor __init__(Abstract)

:since: v0.2.00
        """

        self.cache = None
        """
Session data cache
        """
        self.user_profile = None
        """
Session user profile
        """
    #

    def __getattr__(self, name):
        """
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Adapter attribute
:since:  v0.2.00
        """

        adapter = Abstract.get_adapter()

        if (adapter is None or (not hasattr(adapter, name))): raise TypeException("Session adapter does not implement '{0}'".format(name))
        return getattr(adapter(self), name)
    #

    def get(self, key = None, default = None):
        """
Returns the value with the specified key or all session values.

:param key: Session key or NULL to receive all session values.
:param default: Default value if not set

:return: (mixed) Value
:since:  v0.2.00
        """

        return (self.cache if (key is None or self.cache is None) else self.cache.get(key, default))
    #

    def get_timeout(self):
        """
Returns the specified session timeout value.

:return: (int) Session timeout value in seconds
:since:  v0.2.00
        """

        raise NotImplementedException()
    #

    def get_user_id(self):
        """
Returns the user ID set for the session.

:return: (str) User ID; None if not set
:since:  v0.2.00
        """

        return (None if (self.cache is None or "session.user_id" not in self.cache) else self.cache['session.user_id'])
    #

    def get_user_profile(self):
        """
Returns the user profile set for the session.

:return: (mixed) User Profile; None if not set
:since:  v0.2.00
        """

        # pylint: disable=broad-except

        _return = None

        try:
            if (self.user_profile is not None): _return = self.user_profile
            else:
                user_id = self.get_user_id()
                user_profile = None

                try:
                    if (user_id is not None):
                        user_profile_class = NamedLoader.get_class("dNG.data.user.Profile")
                        if (user_profile_class is not None): user_profile = user_profile_class.load_id(user_id)
                    #
                except NothingMatchedException: pass

                if (user_profile is not None and user_profile.is_valid()):
                    self.user_profile = user_profile
                    _return = self.user_profile
                #
            #
        except Exception as handled_exception:
            LogLine.error(handled_exception, context = "pas_session")
            _return = None
        #

        return _return
    #

    def get_uuid(self):
        """
Returns the uuID of this session instance.

:return: (str) uuID
:since:  v0.2.00
        """

        raise NotImplementedException()
    #

    def is_active(self):
        """
Returns true if the uuID session is in use.

:return: (bool) True if in use
:since:  v0.2.00
        """

        return False
    #

    def is_persistent(self):
        """
Returns true if the uuID session is set persistently at the client.

:return: (bool) True if set
:since:  v0.2.00
        """

        adapter = Abstract.get_adapter()
        return (False if (adapter is None) else adapter(self).is_persistent())
    #

    def is_valid(self):
        """
Returns true if the uuID session is still valid.

:return: (bool) True if valid
:since:  v0.2.00
        """

        return False
    #

    def save(self):
        """
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since:  v0.2.00
        """

        adapter = Abstract.get_adapter()
        return (False if (adapter is None) else adapter(self).save())
    #

    def set(self, key, value = None):
        """
Sets the value for the specified key.

:param key: Key
:param value: Value

:since: v0.2.00
        """

        if (self.cache is None): self.cache = { }
        if (key == "session.user_id"): self.user_profile = None
        self.cache[key] = value
    #

    def set_timeout(self, timeout = None):
        """
Sets the specified session timeout value.

:param timeout: Session timeout value in seconds

:since: v0.2.00
        """

        raise NotImplementedException()
    #

    def set_thread_default(self):
        """
Sets this session as the thread default one.

:since: v0.2.00
        """

        store = AbstractResponse.get_instance_store()
        if (store is not None): store['dNG.data.session.uuid'] = self.get_uuid()
    #

    def unset(self, key):
        """
Unsets the specified key.

:param key: Key

:since: v0.2.00
        """

        if (key == "session.user_id"): self.user_profile = None
        if (self.cache is not None and key in self.cache): del(self.cache[key])
    #

    @staticmethod
    def get_adapter():
        """
Returns the session adapter for protocol specific methods.

:return: (object) Session protocol adapter; None if not set
:since:  v0.2.00
        """

        store = AbstractResponse.get_instance_store()
        return (store['dNG.data.session.Adapter'] if (store is not None and "dNG.data.session.Adapter" in store) else None)
    #

    @staticmethod
    def load(uuid = None, session_create = True):
        """
Loads the given (or initializes a fresh) uuID.

:param uuid: Unique user identification
:param session_create: Create a new session if no one is loaded

:since: v0.2.00
        """

        raise NotImplementedException()
    #

    @staticmethod
    def set_adapter(adapter):
        """
Sets the protocol specific adapter to be called.

:param adapter: Session protocol adapter

:since: v0.2.00
        """

        if (issubclass(adapter, AbstractAdapter)):
            store = AbstractResponse.get_instance_store()
            if (store is not None): store['dNG.data.session.Adapter'] = adapter
        #
    #
#
