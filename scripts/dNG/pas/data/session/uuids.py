# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.session.Uuids
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

from random import randrange
from time import time

from dNG.data.json_parser import JsonParser
from dNG.pas.data.settings import Settings
from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
from dNG.pas.database.instances.uuids import Uuids as UuidsInstance
from .abstract import Abstract

class Uuids(Abstract, Instance):
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

		Abstract.__init__(self)

		if (db_instance == None): db_instance = UuidsInstance()
		Instance.__init__(self, db_instance)

		self.session_time = int(Settings.get("pas_session_uuids_session_time", 900))
		"""
Max age of the session
		"""
		self.validity = None
		"""
Validity of the session
		"""

		if (self._db_instance.data != None and self._db_instance.data != ""): self.cache = JsonParser().json2data(self._db_instance.data)
		if (self._db_instance.session_timeout == None): self._db_instance.session_timeout = int(time() + self.session_time)
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

	def is_valid(self):
	#
		"""
Returns true if the uuID session is still valid.

:param uuid: Unique user identification

:since: v0.1.00
		"""

		if (self.validity == None):
		#
			if (self._db_instance == None): raise RuntimeError("Database instance is not correctly initialized", 22)
			_return = (self._db_instance.session_timeout > time())

			if (_return):
			#
				adapter = Uuids.get_adapter()
				if (adapter != None): _return = adapter(self).is_valid()
			#

			self.validity = _return
		#
		else: _return = self.validity

		return _return
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
			if (self._db_instance == None): raise RuntimeError("Database instance is not correctly initialized", 22)
			_return = Abstract.save(self)

			if (_return):
			#
				self._db_instance.session_timeout = int(time() + self.session_time)
				self._db_instance.data = ("" if (self.cache == None) else JsonParser().data2json(self.cache))

				Instance.save(self)
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

:since: v0.1.00
		"""

		if (uuid == None): uuid = Uuids.get_uuid()
		database = Connection.get_instance()

		if ((not Settings.get("pas_database_auto_maintenance", False)) and randrange(0, 3) < 1):
		#
			if (database.query(UuidsInstance).filter(UuidsInstance.session_timeout <= int(time())).delete() > 0): database.optimize_random(UuidsInstance)
		#

		_return = None
		db_instance = (None if (uuid == None) else database.query(UuidsInstance).filter(UuidsInstance.uuid == uuid).first())

		if (db_instance != None):
		#
			_return = Uuids(db_instance)

			adapter = Uuids.get_adapter()
			if (adapter != None): adapter(_return).load()

			if (not _return.is_valid()):
			#
				database.delete(db_instance)
				_return = None
			#
		#

		if (_return == None and session_create): _return = Uuids()

		if (_return != None):
		#
			uuids_data = _return.data_get("uuid")
			Uuids.set_uuid(uuids_data['uuid'])
		#

		return _return
	#
#

##j## EOF