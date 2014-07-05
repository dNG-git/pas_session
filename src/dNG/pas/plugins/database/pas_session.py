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

# pylint: disable=unused-argument

from dNG.pas.database.schema import Schema
from dNG.pas.module.named_loader import NamedLoader
from dNG.pas.plugins.hook import Hook

def after_apply_schema(params, last_return = None):
#
	"""
Called for "dNG.pas.Database.applySchema.after"

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	uuids_class = NamedLoader.get_class("dNG.pas.database.instances.Uuids")
	Schema.apply_version(uuids_class)

	return last_return
#

def load_all(params, last_return = None):
#
	"""
Load and register all SQLAlchemy objects to generate database tables.

:param params: Parameter specified
:param last_return: The return value from the last hook called.

:return: (mixed) Return value
:since:  v0.1.00
	"""

	NamedLoader.get_class("dNG.pas.database.instances.Uuids")
	return last_return
#

def register_plugin():
#
	"""
Register plugin hooks.

:since: v0.1.00
	"""

	Hook.register("dNG.pas.Database.applySchema.after", after_apply_schema)
	Hook.register("dNG.pas.Database.loadAll", load_all)
#

def unregister_plugin():
#
	"""
Unregister plugin hooks.

:since: v0.1.00
	"""

	Hook.unregister("dNG.pas.Database.applySchema.after", after_apply_schema)
	Hook.unregister("dNG.pas.Database.loadAll", load_all)
#

##j## EOF