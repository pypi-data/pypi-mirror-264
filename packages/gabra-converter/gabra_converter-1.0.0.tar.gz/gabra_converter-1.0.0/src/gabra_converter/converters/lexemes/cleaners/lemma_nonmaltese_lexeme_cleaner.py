'''
Skip any lexemes whose lemma contains non-Maltese letters.
'''

from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner


__all__ = [
    'LemmaNonmalteseLexemeCleaner',
]


MALTESE_LETTERS = set(' abċdefġghħijklmnopqrstuvwxżzàèìòù\'')


#########################################
class LemmaNonmalteseLexemeCleaner(LexemeCleaner):
    '''
    Skip any lexemes whose lemma contains non-Maltese letters.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__(
            id_='lemma_nonmaltese',
            description='Skip any lexemes whose lemma contains non-Maltese letters.',
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
        return set(row.lemma.lower()) <= MALTESE_LETTERS
