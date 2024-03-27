'''
Skip any wordforms whose lexeme is missing.
'''

from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner import WordformCleaner


__all__ = [
    'MissingLexemeWordformCleaner',
]


#########################################
class MissingLexemeWordformCleaner(WordformCleaner):
    '''
    Skip any wordforms whose lexeme is missing.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__(
            id_='missing_lexeme',
            description='Skip any wordforms whose lexeme ID does not refer to an existing lexeme.',
        )

    #########################################
    def clean(
        self,
        row: WordformRow, # pylint: disable=unused-argument
        lexemes_id_map: dict[str, int], # pylint: disable=unused-argument
    ) -> bool:
        '''
        Clean a row using a particular process.

        :param row: A wordform row to be checked and cleaned.
        :param lexemes_id_map: A dictionary mapping the original lexeme hexademical unique IDs to
            their given decimal unique IDs.
        :return: Whether the row passes the cleaner's filter.
            A False indicates that it should be skipped.
        '''
        return row.lexeme_id.oid in lexemes_id_map
