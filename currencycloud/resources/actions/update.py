'''This module provides the Update Mixin'''


class UpdateMixin(object):
    '''This mixin allows a Resource to be changed on the CurrencyCloud servers'''

    def update(self):
        '''Send the updated fields to CurrencyCloud'''
        self._client.update(self.id, **self.changed_items)
        self.changed_attributes.clear()
        return self
