# -*- coding: utf-8 -*-
##j## BOF

"""
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
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, db_instance = None):
	#
		"""
Constructor __init__(Uuids)

:since: v0.1.00
		"""

		Implementation.__init__(self)

		if (db_instance == None): db_instance = _DbUuids()
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

		if (self.local.db_instance.data != None and self.local.db_instance.data != ""): self.cache = JsonResource().json_to_data(self.local.db_instance.data)
		if (self.local.db_instance.session_timeout == None): self.local.db_instance.session_timeout = int(time() + self.session_time)
	#

	def delete(self):
	#
		"""
Deletes this entry from the database.

:since: v0.1.00
		"""

		if (self.log_handler != None): self.log_handler.debug("#echo(__FILEPATH__)# -{0!r}.delete()- (#echo(__LINE__)#)", self, context = "pas_database")
		_return = False

		with self:
		#
			self._database.delete(self.local.db_instance)
			_return = True
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

		return (self.cache != None)
	#

	def is_reloadable(self):
	#
		"""
Returns true if the instance can be reloaded automatically in another
thread.

:return: (bool) True if reloadable
:since:  v0.1.00
		"""

		return (self.uuid != None)
	#

	def is_valid(self):
	#
		"""
Returns true if the uuID session is still valid.

:param uuid: Unique user identification

:since: v0.1.00
		"""

		if (self.validity == None):
		#
			with self:
			#
				_return = (self.local.db_instance.session_timeout > time())

				if (_return):
				#
					adapter = Uuids.get_adapter()
					if (adapter != None): _return = adapter(self).is_valid()
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

		with self._lock:
		#
			if ((not hasattr(self.local, "db_instance")) or self.local.db_instance == None):
			#
				if (self.uuid == None): raise IOException("Database instance is not reloadable.")
				self.local.db_instance = self._database.query(Uuids).filter(_DbUuids.uuid == self.uuid).one()
			#
			else: Instance._reload(self)
		#
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
					self.local.db_instance.session_timeout = int(time() + self.session_time)
					self.local.db_instance.data = ("" if (self.cache == None) else Binary.utf8(JsonResource().data_to_json(self.cache)))

					Instance.save(self)
				#
			#
		#

		return _return
	#

	def set_session_time(self, seconds = None):
	#
		"""
Sets the specified session timeout value.

:param seconds: Session timeout in seconds

:since: v0.1.00
		"""

		self.session_time = seconds
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

		with Connection.get_instance() as database:
		#
			if (uuid == None): uuid = Uuids.get_uuid()

			if ((not Settings.get("pas_database_auto_maintenance", False)) and randrange(0, 3) < 1):
			#
				if (database.query(_DbUuids).filter(_DbUuids.session_timeout <= int(time())).delete() > 0): database.optimize_random(_DbUuids)
			#

			_return = None
			db_instance = (None if (uuid == None) else database.query(_DbUuids).get(uuid))

			if (db_instance != None):
			#
				_return = Uuids(db_instance)

				adapter = Uuids.get_adapter()
				if (adapter != None): adapter(_return).load()

				if (not _return.is_valid()):
				#
					_return.delete()
					_return = None
				#
			#

			if (_return == None and session_create): _return = Uuids()

			if (_return != None):
			#
				uuids_data = _return.get_data_attributes("uuid")
				Uuids.set_uuid(uuids_data['uuid'])
			#
		#

		return _return
	#
#

##j## EOF