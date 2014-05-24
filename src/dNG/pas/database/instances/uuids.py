# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.database.instances.Uuids
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

from sqlalchemy import Column, TEXT, VARCHAR
from uuid import uuid4 as uuid

from dNG.pas.database.types.date_time import DateTime
from .abstract import Abstract

class Uuids(Abstract):
#
	"""
The unique user Identification Service is the SQLAlchemy based database
instance for a session.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.1.00
:license:    http://www.direct-netware.de/redirect.py?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	__tablename__ = "{0}_uuids".format(Abstract.get_table_prefix())
	"""
SQLAlchemy table name
	"""
	db_instance_class = "dNG.pas.data.session.Uuids"
	"""
Encapsulating SQLAlchemy database instance class name
	"""

	uuid = Column(VARCHAR(32), server_default = "", primary_key = True, nullable = False)
	"""
uuids.uuid
	"""
	session_timeout = Column(DateTime, index = True, nullable = False)
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

	def __init__(self, *args, **kwargs):
	#
		"""
Constructor __init__(Uuids)

:since: v0.1.00
		"""

		Abstract.__init__(self, *args, **kwargs)
		if (self.uuid == None): self.uuid = uuid().hex
	#
#

##j## EOF