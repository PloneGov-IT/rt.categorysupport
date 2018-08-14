# -*- coding: utf-8 -*-
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from rt.categorysupport import _
from zope import schema
from zope.interface import implementer
from zope.interface import alsoProvides


class ICategory(model.Schema):

    model.fieldset(
        'taxonomies',
        label=_(u'taxonomies', default=u'Taxonomies'),
        fields=['taxonomies'],
    )

    taxonomies = schema.Tuple(
        title=_(u'taxonomies', default=u'Taxonomies'),
        value_type=schema.TextLine(),
        required=False,
        missing_value=None,
    )
    directives.widget(
        'taxonomies',
        AjaxSelectFieldWidget,
        vocabulary='rt.categorysupport.category_list',
        pattern_options={
            'allowNewItems': False
        }
    )


alsoProvides(ICategory, IFormFieldProvider)


@implementer(ICategory)
class Category(object):

    def __init__(self, context):
        self.context = context
