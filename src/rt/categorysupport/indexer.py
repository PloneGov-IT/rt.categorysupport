# -*- coding: utf-8 -*-
from rt.categorysupport.behaviors.category import ICategory
from plone.indexer import indexer


@indexer(ICategory)
def taxonomies(object, **kw):
    return getattr(object, 'taxonomies', None)
