'''
Remove new lines from the glosses and examples of lexemes.
'''

from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner


__all__ = [
    'NewLinesLexemeCleaner',
]


#########################################
class NewLinesLexemeCleaner(LexemeCleaner):
    '''
    Remove new lines from the glosses and examples of lexemes.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__(
            id_='new_lines',
            description='Remove new lines from the glosses and examples of lexemes.',
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
        if row.glosses is not None:
            for obj in row.glosses:
                obj.gloss = obj.gloss.replace('\n', '')
                if obj.examples is not None:
                    for obj2 in obj.examples:
                        obj2.example = obj2.example.replace('\n', '')
        return True
