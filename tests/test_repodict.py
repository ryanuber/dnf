# Copyright (C) 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#

from dnf.exceptions import RepoError
from dnf.repo import Repo
from tests import mock, support
import dnf.repodict
import operator
import unittest

class TestMultiCall(unittest.TestCase):
    def test_multi_call(self):
        l = dnf.repodict.MultiCallList(["one", "two", "three"])
        self.assertEqual(l.upper(), ["ONE", "TWO", "THREE"])
        self.assertEqual(l.pop(), "three")

    def test_assignment(self):
        o1 = mock.Mock(x=3)
        o2 = mock.Mock(x=5)
        l = dnf.repodict.MultiCallList([o1, o2])
        l.x = 5
        self.assertEqual([5, 5], map(operator.attrgetter('x'), [o1, o2]))

class TestRepoDict(unittest.TestCase):
    def setUp(self):
        self.x  = support.MockRepo('x')
        self.xx = support.MockRepo('xx')
        self.y  = support.MockRepo('y')
        self.z  = support.MockRepo('z')

        self.repos = dnf.repodict.RepoDict()
        self.repos.add(self.x)
        self.repos.add(self.xx)
        self.repos.add(self.y)
        self.repos.add(self.z)
        self.full_set = {self.x, self.xx, self.y, self.z}

    def test_any_enabled(self):
        self.assertTrue(self.repos.any_enabled())
        self.repos.get_multiple("*").disable()
        self.assertFalse(self.repos.any_enabled())

    def test_enabled(self):
        self.assertSequenceEqual(self.repos.enabled(),
                                 list(self.repos.iter_enabled()))

    def test_getmultiple(self):
        self.assertEqual(self.repos['x'], self.x)
        self.assertItemsEqual(self.repos.get_multiple('*'), self.full_set)
        self.assertItemsEqual(self.repos.get_multiple('y'), {self.y})
        self.assertItemsEqual(self.repos.get_multiple('x*'), {self.x, self.xx})

        self.assertRaises(RepoError, self.repos.get_multiple, 'nope')

    def test_iter_enabled(self):
        self.assertItemsEqual(self.repos.iter_enabled(), self.full_set)
        self.repos.get_multiple("x*").disable()
        self.assertItemsEqual(self.repos.iter_enabled(), {self.y, self.z})

    def test_all(self):
        self.assertItemsEqual(self.repos.all, self.full_set)
