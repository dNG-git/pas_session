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

from uuid import uuid4 as uuid

from dNG.database.types.date_time import DateTime

from sqlalchemy.schema import Column
from sqlalchemy.types import TEXT, VARCHAR

from .abstract import Abstract

class Uuids(Abstract):
    """
The unique user Identification Service is the SQLAlchemy based database
instance for a session.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas
:subpackage: session
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    __tablename__ = "{0}_uuids".format(Abstract.get_table_prefix())
    """
SQLAlchemy table name
    """
    db_instance_class = "dNG.data.session.Uuids"
    """
Encapsulating SQLAlchemy database instance class name
    """
    db_schema_version = 1
    """
Database schema version
    """

    uuid = Column(VARCHAR(32), primary_key = True, nullable = False)
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
        """
Constructor __init__(Uuids)

:since: v0.2.00
        """

        Abstract.__init__(self, *args, **kwargs)
        if (self.uuid is None): self.uuid = uuid().hex
    #
#
