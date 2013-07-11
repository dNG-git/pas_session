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
from sqlalchemy import BIGINT, Column, TEXT, VARCHAR
from time import time
from uuid import uuid4 as uuid

from dNG.data.json_parser import JsonParser
from dNG.pas.data.settings import Settings
from dNG.pas.database.connection import Connection
from dNG.pas.database.instance import Instance
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

	__tablename__ = "{0}_uuids".format(Instance.get_table_prefix())
	"""
SQLAlchemy table name
	"""

	db_uuid = Column("uuid", VARCHAR(32), server_default = "", primary_key = True, nullable = False)
	"""
uuids.uuid
	"""
	db_session_timeout = Column("session_timeout", BIGINT, index = True, nullable = False)
	"""
uuids.session_timeout
	"""
	db_ip = Column("ip", VARCHAR(100), server_default = "", nullable = False)
	"""
uuids.ip
	"""
	db_data = Column("data", TEXT, nullable = False)
	"""
uuids.data
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Uuids)

:since: v0.1.00
		"""

		Abstract.__init__(self)
		Instance.__init__(self)

		self.session_time = int(Settings.get("pas_session_uuids_session_time", 900))
		"""
Max age of the session
		"""
		self.validity = None
		"""
Validity of the session
		"""

		if (self.db_uuid == None): self.db_uuid = uuid().hex
		if (self.db_session_timeout == None): self.db_session_timeout = int(time() + self.session_time)
		if (self.db_data != None and self.db_data != ""): self.cache = JsonParser().json2data(self.db_data)
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
			_return = (self.db_session_timeout > time())

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
			_return = Abstract.save(self)

			if (_return):
			#
				self.db_session_timeout = int(time() + self.session_time)
				self.db_data = ("" if (self.cache == None) else JsonParser().data2json(self.cache))

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
			if (database.query(Uuids).filter(Uuids.db_session_timeout <= int(time())).delete() > 0): database.optimize_random(Uuids)
		#

		_return = (None if (uuid == None) else database.query(Uuids).filter(Uuids.db_uuid == uuid).first())

		if (_return != None):
		#
			adapter = Uuids.get_adapter()
			if (adapter != None): adapter(_return).load()

			if (not _return.is_valid()):
			#
				database.delete(_return)
				_return = None
			#
		#

		if (_return == None and session_create): _return = Uuids()
		if (_return != None): Uuids.set_uuid(_return.db_uuid)

		return _return
	#
#

##j## EOF