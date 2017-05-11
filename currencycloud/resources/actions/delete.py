'''This module provides the Delete Mixin'''


class DeleteMixin(object):
    '''This mixin allows a Resource to be delete from CurrencyCloud servers'''

    def delete(self):
        '''Delete the resource from CurrencyCloud'''
        self._client.delete(self.id)
        return self
