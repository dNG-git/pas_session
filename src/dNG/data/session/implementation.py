# -*- coding: utf-8 -*-
##j## BOF

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

from dNG.controller.abstract_request import AbstractRequest
from dNG.controller.abstract_response import AbstractResponse
from dNG.data.settings import Settings
from dNG.module.named_loader import NamedLoader

from .abstract import Abstract

class Implementation(object):
#
	"""
A session is used for stateless requests that want to save data across
multiple responses.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	@staticmethod
	def get_class():
	#
		"""
Returns an session instance based on the configuration set.

:return: (object) HTTP server implementation
:since:  v0.2.00
		"""

		Settings.read_file("{0}/settings/pas_session.json".format(Settings.get("path_data")))
		session_implementation = Settings.get("pas_session_implementation", "Uuids")

		return NamedLoader.get_class("dNG.data.session.{0}".format(session_implementation))
	#

	@staticmethod
	def get_request_uuid():
	#
		"""
Returns the uuID for the corresponding request (if set).

:return: (str) Unique user identification
:since:  v0.2.00
		"""

		instance = AbstractRequest.get_instance()
		return (None if (instance is None) else instance.get_parameter("uuid", None))
	#

	@staticmethod
	def get_session_user_id(session):
	#
		"""
Returns the user ID of the given session instance.

:param session: Session instance

:return: (str) User ID
:since:  v0.2.00
		"""

		return (session.get_user_id() if (isinstance(session, Abstract)) else None)
	#

	@staticmethod
	def get_thread_uuid():
	#
		"""
Returns the uuID set or for the corresponding request (if set).

:return: (str) Unique user identification
:since:  v0.2.00
		"""

		store = AbstractResponse.get_instance_store()
		uuid = (None if (store is None) else store.get("dNG.data.session.uuid"))

		if (uuid is None):
		#
			adapter = Abstract.get_adapter()
			if (adapter is not None): uuid = adapter.get_uuid()
		#

		return (Implementation.get_request_uuid() if (uuid is None) else uuid)
	#

	@staticmethod
	def load(uuid = None, session_create = True):
	#
		"""
Loads the given (or initializes a fresh) uuID.

:param uuid: Unique user identification
:param session_create: Create a new session if no one is loaded

:since: v0.2.00
		"""

		return Implementation.get_class().load(uuid, session_create)
	#

	@staticmethod
	def set_thread_uuid(uuid):
	#
		"""
Defines the uuID for the calling thread.

:param uuid: Unique user identification

:since: v0.2.00
		"""

		store = AbstractResponse.get_instance_store()
		if (store is not None): store['dNG.data.session.uuid'] = uuid
	#
#

##j## EOF