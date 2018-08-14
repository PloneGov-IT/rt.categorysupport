# -*- coding: utf-8 -*-
from rt.categorysupport import _
from plone.supermodel import model
from zope import schema
from plone.app.registry.browser import controlpanel


class ITaxonomySettingsSchema(model.Schema):
    category_list = schema.List(
        title=_(u'category_list', default=u'Category list'),
        default=[],
        missing_value=[],
        value_type=schema.TextLine()
    )


class TaxonomySettings(controlpanel.RegistryEditForm):
    schema = ITaxonomySettingsSchema
    id = u'TaxonomySettings'
    label = _(u'taxonomy_settings', default=u'Taxonomy Settings')


class TaxonomySettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TaxonomySettings
