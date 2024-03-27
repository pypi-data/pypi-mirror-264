'''
Skip any lexemes whose pending field is not set to false.
'''

from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner


__all__ = [
    'PendingLexemeCleaner',
]


#########################################
class PendingLexemeCleaner(LexemeCleaner):
    '''
    Skip any lexemes whose pending field is not set to false.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__(
            id_='pending',
            description='Skip any lexemes whose pending field is not set to false.',
        )

    #########################################
    def clean(
        self,
        row: LexemeRow,
    ) -> bool:
        '''
        Clean a row using a particular process.

        :param row: A lexeme row to be checked and cleaned.
        :return: Whether the row passes the cleaner's filter.
            A False indicates that it should be skipped.
        '''
        return row.pending is False
