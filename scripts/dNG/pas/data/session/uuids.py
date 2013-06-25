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

from binascii import hexlify
from os import urandom
from random import randrange
from sqlalchemy import BIGINT, Column, TEXT, VARCHAR
from time import time

from dNG.data.json_parser import JsonParser
from dNG.pas.data.binary import Binary
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

	uuid = Column(VARCHAR(32), server_default = "", primary_key = True, nullable = False)
	"""
uuids.uuid
	"""
	session_timeout = Column(BIGINT, index = True, nullable = False)
	"""
uuids.session_timeout
	"""
	ip = Column(VARCHAR(100), server_default = "", nullable = False)
	"""
uuids.ip
	"""
	data = Column(TEXT, nullable = False)
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

		if (self.data != None and self.data != ""): self.cache = JsonParser().json2data(self.data)
		if (self.session_timeout == None): self.session_timeout = int(time() + self.session_time)
		if (self.uuid == None): self.uuid = Binary.str(hexlify(urandom(16)))
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
			var_return = (self.session_timeout > time())

			if (var_return):
			#
				adapter = Uuids.get_adapter()
				if (adapter != None): var_return = adapter(self).is_valid()
			#

			self.validity = var_return
		#
		else: var_return = self.validity

		return var_return
	#

	"""
	@hybrid_property
	def value(self):
		return self._value

	@value.setter
	def value(self, value):
		self._value = value
	"""

	def save(self):
	#
		"""
Saves changes of the uuIDs instance.

:return: (bool) True on success
:since:  v0.1.00
		"""

		var_return = False

		if (self.is_valid()):
		#
			var_return = Abstract.save(self)

			if (var_return):
			#
				self.data = ("" if (self.cache == None) else JsonParser().data2json(self.cache))
				self.session_timeout = int(time() + self.session_time)

				if (not self.is_known()): self.insert()
			#
		#

		return var_return
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

		if ((not Settings.get("pas_session_uuids_auto_maintenance", False)) and randrange(0, 3) < 1):
		#
			if (database.query(Uuids).filter(Uuids.session_timeout <= int(time())).delete() > 0): database.optimize_random(Uuids)
		#

		var_return = (None if (uuid == None) else database.query(Uuids).filter(Uuids.uuid == uuid).first())

		if (var_return != None and (not var_return.is_valid())):
		#
			database.delete(var_return)
			var_return = None
		#

		if (var_return == None and session_create): var_return = Uuids()

		if (var_return != None):
		#
			adapter = Uuids.get_adapter()
			if (adapter != None): adapter(var_return).load()

			Uuids.set_uuid(var_return.uuid)
		#

		return var_return
	#
#

##j## EOF