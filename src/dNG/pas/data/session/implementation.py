# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.session.Implementation
"""
"""n// NOTE
----------------------------------------------------------------------------
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
http://www.direct-netware.de/redirect.py?pas;session

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
http://www.direct-netware.de/redirect.py?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasSessionVersion)#
#echo(__FILEPATH__)#
----------------------------------------------------------------------------
NOTE_END //n"""

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.controller.abstract_response import AbstractResponse
from dNG.pas.data.settings import Settings
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.data.user.profile import Profile
from dNG.pas.database.nothing_matched_exception import NothingMatchedException
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.type_exception import TypeException
from .abstract_adapter import AbstractAdapter

class Implementation(object):
#
	"""
A session is used for stateless requests that want to save data across
multiple responses.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	# pylint: disable=unused-argument

	def __init__(self):
	#
		"""
Constructor __init__(Implementation)

:since: v0.1.00
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
	#
		"""
python.org: Called when an attribute lookup has not found the attribute in
the usual places (i.e. it is not an instance attribute nor is it found in the
class tree for self).

:param name: Attribute name

:return: (mixed) Adapter attribute
:since:  v0.1.00
		"""

		adapter = Implementation.get_adapter()

		if (adapter == None or (not hasattr(adapter, name))): raise TypeException("Session adapter does not implement '{0}'".format(name))
		return getattr(adapter(self), name)
	#

	def get(self, key = None, default = None):
	#
		"""
Returns the value with the specified key or all session values.

:param key: Session key or NULL to receive all session values.
:param default: Default value if not set

:return: (mixed) Value
:since:  v0.1.00
		"""

		return (self.cache if (key == None or self.cache == None) else self.cache.get(key, default))
	#

	def get_user_id(self):
	#
		"""
Returns the user ID set for the session.

:return: (str) User ID; None if not set
:since:  v0.1.00
		"""

		return (None if (self.cache == None or "session.user_id" not in self.cache) else self.cache['session.user_id'])
	#

	def get_user_profile(self):
	#
		"""
Returns the user profile set for the session.

:return: (mixed) User Profile; None if not set
:since:  v0.1.00
		"""

		# pylint: disable=broad-except

		_return = None

		try:
		#
			if (self.user_profile != None): _return = self.user_profile
			else:
			#
				user_id = self.get_user_id()
				user_profile = None

				try:
				#
					if (user_id != None): user_profile = Profile.load_id(user_id)
				#
				except NothingMatchedException: pass

				if (user_profile != None and user_profile.is_valid()):
				#
					self.user_profile = user_profile
					_return = self.user_profile
				#
			#
		#
		except Exception as handled_exception:
		#
			LogLine.error(handled_exception)
			_return = None
		#

		return _return
	#

	def is_active(self):
	#
		"""
Returns true if the uuID session is in use.

:param uuid: Unique user identification

:return: (bool) True if in use
:since:  v0.1.00
		"""

		return False
	#

	def is_persistent(self):
	#
		"""
Returns true if the uuID session is set persistently at the client.

:return: (bool) True if set
:since:  v0.1.00
		"""

		adapter = Implementation.get_adapter()
		return (False if (adapter == None) else adapter(self).is_persistent())
	#

	def is_valid(self):
	#
		"""
Returns true if the uuID session is still valid.

:return: (bool) True if valid
:since:  v0.1.00
		"""

		return False
	#

	def save(self):
	#
		"""
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since:  v0.1.00
		"""

		adapter = Implementation.get_adapter()
		return (False if (adapter == None) else adapter(self).save())
	#

	def set(self, key, value = None):
	#
		"""
Sets the value for the specified key.

:param key: Settings key
:param value: Value

:since: v0.1.00
		"""

		if (self.cache == None): self.cache = { }
		if (key == "session.user_id"): self.user_profile = None
		self.cache[key] = value
	#

	def set_session_timeout(self, timeout = None):
	#
		"""
Sets the specified session timeout value.

:param timeout: Session timeout value

:since: v0.1.00
		"""

		pass
	#

	@staticmethod
	def get_adapter():
	#
		"""
Return the session adapter for protocol specific methods.

:return: (object) Session protocol adapter; None if not set
:since:  v0.1.00
		"""

		store = AbstractResponse.get_instance_store()
		return (store['dNG.pas.data.session.Adapter'] if (store != None and "dNG.pas.data.session.Adapter" in store) else None)
	#

	@staticmethod
	def get_class():
	#
		"""
Returns an session instance based on the configuration set.

:return: (object) HTTP server implementation
:since:  v0.1.00
		"""

		Settings.read_file("{0}/settings/pas_session.json".format(Settings.get("path_data")))
		session_implementation = Settings.get("pas_session_implementation", "Uuids")

		return NamedLoader.get_class("dNG.pas.data.session.{0}".format(session_implementation))
	#

	@staticmethod
	def get_request_uuid():
	#
		"""
Returns the uuID for the corresponding request (if set).

:return: (str) Unique user identification
:since:  v0.1.00
		"""

		instance = AbstractRequest.get_instance()
		return (None if (instance == None) else instance.get_parameter("uuid", None))
	#

	@staticmethod
	def get_uuid():
	#
		"""
Returns the uuID set or for the corresponding request (if set).

:return: (str) Unique user identification
:since:  v0.1.00
		"""

		store = AbstractResponse.get_instance_store()
		uuid = None

		if (store != None): uuid = (store['dNG.pas.data.session.uuid'] if ("dNG.pas.data.session.uuid" in store) else None)

		if (uuid == None):
		#
			adapter = Implementation.get_adapter()
			if (adapter != None): uuid = adapter.get_uuid()
		#

		return (Implementation.get_request_uuid() if (uuid == None) else uuid)
	#

	@staticmethod
	def load(uuid = None, session_create = True):
	#
		"""
Loads the given (or initializes a fresh) uuID.

:param uuid: Unique user identification
:param session_create: Create a new session if no one is loaded

:since: v0.1.00
		"""

		raise NotImplementedException()
	#

	@staticmethod
	def set_adapter(adapter):
	#
		"""
Sets the protocol specific adapter to be called.

:param adapter: Session protocol adapter

:since: v0.1.00
		"""

		if (issubclass(adapter, AbstractAdapter)):
		#
			store = AbstractResponse.get_instance_store()
			if (store != None): store['dNG.pas.data.session.Adapter'] = adapter
		#
	#

	@staticmethod
	def set_uuid(uuid):
	#
		"""
Defines the uuID for the calling thread.

:param uuid: Unique user identification

:since: v0.1.00
		"""

		store = AbstractResponse.get_instance_store()
		if (store != None): store['dNG.pas.data.session.uuid'] = uuid
	#
#

##j## EOF