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

from random import randrange
from time import time

from dNG.data.json_resource import JsonResource
from dNG.pas.data.binary import Binary
from dNG.pas.data.settings import Settings
from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
from dNG.pas.database.instances.uuids import Uuids as _DbUuids
from dNG.pas.runtime.io_exception import IOException
from .implementation import Implementation

class Uuids(Instance, Implementation):
#
	"""
The unique user Identification Service is the database based default
session implementation.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(Uuids)

:since: v0.1.00
		"""

		Implementation.__init__(self)

		if (db_instance is None): db_instance = _DbUuids()
		Instance.__init__(self, db_instance)

		self.session_time = int(Settings.get("pas_session_uuids_session_time", 900))
		"""
Max age of the session
		"""
		self.uuid = db_instance.uuid
		"""
Database uuID used for reloading
		"""
		self.validity = None
		"""
Validity of the session
		"""

		if (self.local.db_instance.data is not None and self.local.db_instance.data != ""): self.cache = JsonResource().json_to_data(self.local.db_instance.data)
		if (self.local.db_instance.session_timeout is None): self.local.db_instance.session_timeout = int(time() + self.session_time)
	#

	def delete(self):
	#
		"""
Deletes this entry from the database.

:since: v0.1.00
		"""

		if (self.log_handler is not None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.delete()- (#echo(__LINE__)#)", self, context = "pas_database")
		_return = False

		with self:
		#
			self._ensure_transaction_context()

			self.local.connection.delete(self.local.db_instance)
			_return = True
		#

		return _return
	#

	def get_timeout(self):
	#
		"""
Returns the specified session timeout value.

:return: (int) Session timeout value in seconds
:since:  v0.1.02
		"""

		_return = self.get_data_attributes("session_timeout")['session_timeout'] - time()
		if (_return < 0): _return = 0

		return _return
	#

	get_uuid = Instance._wrap_getter("uuid")
	"""
Returns the uuID of this session instance.

:return: (str) uuID
:since:  v0.1.00
	"""

	def is_active(self):
	#
		"""
Returns true if the uuID session is in use.

:param uuid: Unique user identification

:return: (bool) True if in use
:since:  v0.1.00
		"""

		return (self.cache is not None)
	#

	def is_reloadable(self):
	#
		"""
Returns true if the instance can be reloaded automatically in another
thread.

:return: (bool) True if reloadable
:since:  v0.1.00
		"""

		return (self.uuid is not None)
	#

	def is_valid(self):
	#
		"""
Returns true if the uuID session is still valid.

:param uuid: Unique user identification

:since: v0.1.00
		"""

		if (self.validity is None):
		#
			with self:
			#
				_return = (self.local.db_instance.session_timeout > time())

				if (_return):
				#
					adapter = Uuids.get_adapter()
					if (adapter is not None): _return = adapter(self).is_valid()
				#

				self.validity = _return
			#
		#
		else: _return = self.validity

		return _return
	#

	def _reload(self):
	#
		"""
Implementation of the reloading SQLAlchemy database instance logic.

:since: v0.1.00
		"""

		if (self.local.db_instance is None):
		#
			if (self.uuid is None): raise IOException("Database instance is not reloadable.")
			self.local.db_instance = self.local.connection.query(Uuids).filter(_DbUuids.uuid == self.uuid).one()
		#
		else: Instance._reload(self)
	#

	def save(self):
	#
		"""
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since:  v0.1.00
		"""

		_return = False

		if (self.is_valid()):
		#
			with self:
			#
				_return = Implementation.save(self)

				if (_return):
				#
					self.local.db_instance.data = ("" if (self.cache is None) else Binary.utf8(JsonResource().data_to_json(self.cache)))
					Instance.save(self)
				#
			#
		#

		return _return
	#

	def set_timeout(self, timeout = None):
	#
		"""
Sets the specified session timeout value.

:param seconds: Session timeout in seconds

:since: v0.1.00
		"""

		if (timeout is not None): self.session_time = timeout
		with self: self.local.db_instance.session_timeout = time() + self.session_time
	#

	@staticmethod
	def load(uuid = None, session_create = True):
	#
		"""
Loads the given (or externally identified) uuID session. Creates a new one
if required and requested.

:param uuid: Unique user identification
:param session_create: Create a new session if no one is loaded

:since: v0.1.00
		"""

		_return = None

		if (uuid is None): uuid = Uuids.get_thread_uuid()

		if (uuid is not None):
		#
			with Connection.get_instance() as connection:
			#
				if ((not Settings.get("pas_database_auto_maintenance", False)) and randrange(0, 3) < 1):
				#
					if (connection.query(_DbUuids).filter(_DbUuids.session_timeout <= int(time())).delete() > 0):
					#
						connection.optimize_random(_DbUuids)
					#
				#

				db_instance = connection.query(_DbUuids).get(uuid)

				if (db_instance is not None):
				#
					_return = Uuids(db_instance)

					adapter = Uuids.get_adapter()
					if (adapter is not None): adapter(_return).load()

					if (not _return.is_valid()):
					#
						_return.delete()
						_return = None
					#
				#
			#
		#

		if (_return is None and session_create): _return = Uuids()

		if (_return is not None):
		#
			uuid = _return.get_uuid()
			Uuids.set_thread_uuid(uuid)
		#

		return _return
	#
#

##j## EOF