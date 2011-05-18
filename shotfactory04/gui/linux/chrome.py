# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
GUI-specific interface functions for X11.
"""

__revision__ = "$Rev: 2747 $"
__date__ = "$Date: 2008-04-09 00:39:48 +1000 (Wed, 09 Apr 2008) $"
__author__ = "$Author: hawk $"


import os
import time
import shutil
from shotfactory04.gui import linux as base
from shotfactory04.inifile import IniFile


class Gui(base.Gui):
    """
    Special functions for Chrome.
    """
    def start_browser(self, config, url, options):
        if config['command']=="":
            config['command']="chrome --user-data-dir=chrome --no-first-run "
        base.Gui.start_browser(self,config,url,options)

    def reset_browser(self):
        """
        Reset crashed state and delete browser cache.
        """
        if os.path.exists("chrome"):
            shutil.rmtree("chrome")
	pass

    def focus_browser(self):
        """
        Focus on the browser window.
        """
        self.shell('xte "mousemove 400 4"')
        self.shell('xte "mouseclick 1"')

    def reuse_browser(self, config, url, options):
        """
        Open a new URL in the same browser window.
        """
        command = config['command'] or config['browser'].lower()
        command = '%s "%s"' % (command, url)
        print "Running", command
        error = self.shell(command)
        if error:
            raise RuntimeError("could not load new URL in the browser")
        print "Sleeping %d seconds while page is loading." % (
            options.reuse_wait)
        time.sleep(options.reuse_wait / 2.0)
        self.maximize()
        time.sleep(options.reuse_wait / 2.0)
