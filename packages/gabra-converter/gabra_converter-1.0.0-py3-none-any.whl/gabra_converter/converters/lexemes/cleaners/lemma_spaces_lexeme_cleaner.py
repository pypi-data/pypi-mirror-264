'''
Skip any lexemes whose lemma contains spaces.
'''

from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner


__all__ = [
    'LemmaSpacesLexemeCleaner',
]


#########################################
class LemmaSpacesLexemeCleaner(LexemeCleaner):
    '''
    Skip any lexemes whose lemma contains spaces.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__(
            id_='lemma_spaces',
            description='Skip any lexemes whose lemma contains spaces.',
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
        return ' ' not in row.lemma
