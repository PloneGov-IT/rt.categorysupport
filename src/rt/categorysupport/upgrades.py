# -*- coding: utf-8 -*-
from plone import api
from rt.categorysupport import logger


default_profile = 'profile-rt.categorysupport:default'


def migrate_to_1001(context):
    setup_tool = api.portal.get_tool('portal_setup')
    setup_tool.runImportStepFromProfile(default_profile, 'catalog')
    logger.info(u'Updated to 1001')
