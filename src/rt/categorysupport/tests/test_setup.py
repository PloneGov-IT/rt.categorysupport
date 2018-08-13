# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from rt.categorysupport.testing import RT_CATEGORYSUPPORT_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that rt.categorysupport is properly installed."""

    layer = RT_CATEGORYSUPPORT_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if rt.categorysupport is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'rt.categorysupport'))

    def test_browserlayer(self):
        """Test that IRtCategorysupportLayer is registered."""
        from rt.categorysupport.interfaces import (
            IRtCategorysupportLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IRtCategorysupportLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = RT_CATEGORYSUPPORT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get(userid=TEST_USER_ID).getRoles()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['rt.categorysupport'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if rt.categorysupport is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'rt.categorysupport'))

    def test_browserlayer_removed(self):
        """Test that IRtCategorysupportLayer is removed."""
        from rt.categorysupport.interfaces import \
            IRtCategorysupportLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IRtCategorysupportLayer,
           utils.registered_layers())
