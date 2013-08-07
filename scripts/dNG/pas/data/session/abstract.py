# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.session.Abstract
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

from threading import local

from dNG.pas.controller.abstract_request import AbstractRequest
from dNG.pas.controller.abstract_response import AbstractResponse
from dNG.pas.data.logging.log_line import LogLine
from dNG.pas.data.user.profile import Profile
from .abstract_adapter import AbstractAdapter

class Abstract(object):
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

	local = local()
	"""
Local data handle
	"""
	thread_safe_mode = True
	"""
True if each running thread represents requests from exactly one client
	"""
	uuid_cookie_mode = None
	"""
Support cookies for uuIDs
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Abstract)

:since: v0.1.00
		"""

		self.cache = None
		"""
Session data cache
		"""
		self.profile = None
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

:return: (callable) Static adapter method
:since:  v0.1.00
		"""

		adapter = Abstract.get_adapter()

		if (adapter != None and hasattr(adapter, name)): return getattr(adapter(self), name)
		else: raise AttributeError("Session adapter does not implement '{0}'".format(name))
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

	def get_user_profile(self):
	#
		"""
Returns the value with the specified key or all session values.

:param key: Session key or NULL to receive all session values.
:param default: Default value if not set

:return: (mixed) Value
:since:  v0.1.00
		"""

		_return = None

		try:
		#
			if (self.profile != None): _return = self.profile
			elif (self.cache != None and "session.user_id" in self.cache and self.cache['session.user_id'] != None):
			#
				user_profile = Profile.load_id(self.cache['session.user_id'])
				user_profile_data = (None if (user_profile == None) else user_profile.data_get("banned", "deleted", "locked"))

				if (user_profile_data != None and user_profile_data['banned'] + user_profile_data['deleted'] + user_profile_data['locked'] == 0):
				#
					self.profile = user_profile
					_return = self.profile
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
Returns true if the uuID session set persistently at the client.

:return: (bool) True if set
:since:  v0.1.00
		"""

		adapter = Abstract.get_adapter()
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

		adapter = Abstract.get_adapter()
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
		if (key == "session.user_id"): self.profile = None
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

		_return = None

		if (not Abstract.thread_safe_mode):
		#
			store = AbstractResponse.get_instance_store()
			if (store != None and "dNG.pas.data.session.adapter" in store): _return = store['dNG.pas.data.session.adapter']
		#
		elif (hasattr(Abstract.local, "adapter")): _return = Abstract.local.adapter

		return _return
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

		if (Abstract.thread_safe_mode): uuid = (Abstract.local.uuid if (hasattr(Abstract.local, "uuid")) else None)
		else:
		#
			store = AbstractResponse.get_instance_store()
			if (store != None): uuid = (store['dNG.pas.data.session.uuid'] if ("dNG.pas.data.session.uuid" in store) else None)
		#

		if (uuid == None):
		#
			adapter = Abstract.get_adapter()
			if (adapter != None): uuid = adapter.get_uuid()
		#

		return (Abstract.get_request_uuid() if (uuid == None) else uuid)
	#

	@staticmethod
	def load(uuid = None):
	#
		"""
Loads the given (or initializes a fresh) uuID.

:param uuid: Unique user identification

:since: v0.1.00
		"""

		raise RuntimeError("Not implemented", 38)
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
			if (Abstract.thread_safe_mode): Abstract.local.adapter = adapter
			else:
			#
				store = AbstractResponse.get_instance_store()
				if (store != None): store['dNG.pas.data.session.adapter'] = adapter
			#
		#
	#

	@staticmethod
	def set_thread_safety(thread_safe):
	#
		"""
Defines the thread safety state.

:param thread_safe: True if each running thread represents requests from
                    exactly one client

:since: v0.1.00
		"""

		Abstract.thread_safe_mode = thread_safe
	#

	@staticmethod
	def set_uuid(uuid):
	#
		"""
Defines the uuID for the calling thread.

:param uuid: Unique user identification

:since: v0.1.00
		"""

		if (Abstract.thread_safe_mode): Abstract.local.uuid = uuid
		else:
		#
			store = AbstractResponse.get_instance_store()
			if (store != None): store['dNG.pas.data.session.uuid'] = uuid
		#
	#
#

##j## EOF