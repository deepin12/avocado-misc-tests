#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: 2021 IBM
# Author: Nageswara R Sastry <rnsastry@linux.ibm.com>

from avocado import Test
from avocado.utils import process
from avocado.utils.software_manager import SoftwareManager


class lparstat(Test):

    def setUp(self):
        sm = SoftwareManager()
        if not sm.check_installed("powerpc-utils-core") and \
           not sm.install("powerpc-utils-core"):
            self.cancel("Fail to install required 'powerpc-utils-core' package")

    def test_list(self):
        lists = self.params.get('list', default=['-i', '-x', '-E', '-l', '1 2'])
        for list_item in lists:
            cmd = "lparstat %s" % list_item
            if process.system(cmd, ignore_status=True, sudo=True):
                self.log.info("%s command failed" % cmd)
                self.fail("lparstat: %s command failed to execute" % cmd)

    def test_nlist(self):
        # Negative tests
        lists = self.params.get('nlist', default=['--nonexistingoption'])
        for list_item in lists:
            cmd = "lparstat %s" % list_item
            if not process.system(cmd, ignore_status=True, sudo=True):
                self.log.info("%s command passed" % cmd)
                self.fail("lparstat: Expected failure, %s command exeucted \
                          successfully." % cmd)
