# -*- coding: utf-8 -*-
##j## BOF

"""
dNG.pas.data.session
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

from dNG.pas.data.settings import Settings
from dNG.pas.module.named_loader import NamedLoader

Session = NamedLoader.get_instance("dNG.pas.data.session.{0}".format(Settings.get("pas_core_session_implementation", "Uuids")), True)

##j## EOF