# -*- coding: utf-8 -*-
from Products.Five import BrowserView
from plone import api


class TaxonomyInfo(BrowserView):
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
