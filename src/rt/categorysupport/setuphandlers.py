# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SchemaInvalidatedEvent
from Products.CMFPlone.interfaces import INonInstallable
from rt.categorysupport import logger
from zope.component import getUtility
from zope.component import queryUtility
from zope.event import notify
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

try:
    from rer.sitesearch.custom_fields import IndexesValueField
    from rer.sitesearch.interfaces import IRERSiteSearchSettings
except Exception:
    pass


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ["rt.categorysupport:uninstall"]


def setRegistyIndexes(context, indexes_list):
    """
    """
    pc = getToolByName(context, "portal_catalog")
    catalog_indexes = pc.indexes()
    new_items = []
    for index in indexes_list:
        index_id = index[0]
        index_title = index[1]
        if index_id in catalog_indexes:
            new_value = IndexesValueField()
            new_value.index = index_id
            new_value.index_title = index_title
            new_items.append(new_value)
    return tuple(new_items)


def post_install(context):
    """Post install script"""

    # get all content type of site
    factory = getUtility(
        IVocabularyFactory, "plone.app.vocabularies.PortalTypes"
    )  # noqa
    vocabulary = factory(context)
    types = [x.value for x in vocabulary]

    # add behaviors to all dexterity content type
    for type in types:
        fti = queryUtility(IDexterityFTI, name=type)
        if not fti:
            continue
        behaviors = [x for x in fti.behaviors]
        behaviors.append(u"rt.categorysupport.behaviors.category.ICategory")
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent(type))

    # new index
    portal = api.portal.get()
    setup_tool = portal.portal_setup
    setup_tool.runImportStepFromProfile(
        "profile-rt.categorysupport:default", "catalog"
    )
    catalog = api.portal.get_tool(name=u"portal_catalog")
    indexes = catalog.indexes()

    wanted = [("taxonomies", "KeywordIndex", {"indexed_attrs": "taxonomies"})]

    indexables = []
    for idx in wanted:
        if idx[0] in indexes:
            logger.info(
                "Found the {0} index in the catalog, nothing "
                "changed.".format(idx[0])
            )
        else:
            catalog.addIndex(name=idx[0], type=idx[1], extra=idx[2])
            logger.info(
                "Added {0} ({1}) to the catalog.".format(idx[0], idx[1])
            )
            indexables.append(idx[0])
    if len(indexables) > 0:
        logger.info("Indexing new indexes {0}.".format(", ".join(indexables)))
        catalog.manage_reindexIndex(ids=indexables)

    # check if rer.sitesearch was installed
    qi = getToolByName(context, "portal_quickinstaller")
    prods = qi.listInstallableProducts(skipInstalled=False)
    prods = [x["id"] for x in prods if x["status"] == "installed"]

    if "rer.sitesearch" in prods:
        # add taxonomies index to rer.siteserach oredering criteria
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IRERSiteSearchSettings, check=False)

        TAXONOMIES_INDEX = [("taxonomies", "Temi"), ("Subject", "Subject")]
        indexes = setRegistyIndexes(context, TAXONOMIES_INDEX)
        settings.available_indexes = indexes

        # aggiungo il campo taxonomies a quelli visibili nella vista
        if "taxonomies" not in settings.indexes_order:
            settings.indexes_order += ("taxonomies",)


def uninstall(context):
    """Uninstall script"""

    # get all content type of site
    factory = getUtility(
        IVocabularyFactory, "plone.app.vocabularies.PortalTypes"
    )  # noqa
    vocabulary = factory(context)
    types = [x.value for x in vocabulary]

    # remove behavior to all dexterity content type
    for type in types:
        fti = queryUtility(IDexterityFTI, name=type)
        if not fti:
            continue
        behaviors = [x for x in fti.behaviors]
        if "rt.categorysupport.behaviors.category.ICategory" in behaviors:
            behaviors.remove("rt.categorysupport.behaviors.category.ICategory")
        fti.behaviors = tuple(behaviors)
        # invalidate schema cache
        notify(SchemaInvalidatedEvent(type))
