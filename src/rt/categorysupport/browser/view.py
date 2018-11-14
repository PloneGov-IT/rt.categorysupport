# -*- coding: utf-8 -*-
from plone.app.contenttypes.browser.folder import FolderView
from plone import api


class TaxonomyInfo(FolderView):
    """  """

    def get_taxonomies(self):
        if self.context:
            tax_dict = {}
            brains = api.content.find(context=self.context)
            for brain in brains:
                obj = brain.getObject()
                if not obj.taxonomies:
                    continue
                for tax in obj.taxonomies:
                    if tax in tax_dict.keys():
                        tax_dict[tax] += 1
                    else:
                        tax_dict[tax] = 1

            return tax_dict

        return {}

    def get_subjects(self):
        if self.context:
            _dict = {}
            brains = api.content.find(context=self.context)
            for brain in brains:
                obj = brain.getObject()
                if not obj.subject:
                    continue
                for el in obj.subject:
                    if el in _dict.keys():
                        _dict[el] += 1
                    else:
                        _dict[el] = 1

            return _dict

        return {}

    def batch(self):
        return super(TaxonomyInfo, self).batch()
