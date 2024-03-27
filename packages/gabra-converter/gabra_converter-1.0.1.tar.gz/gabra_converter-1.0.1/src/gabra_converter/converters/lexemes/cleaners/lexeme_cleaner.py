'''
Clean or flag for skipping a lexeme row based on some condition.
'''

from abc import ABC
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow


__all__ = [
    'LexemeCleaner',
]


#########################################
class LexemeCleaner(ABC):
    '''
    Abstract class to be inherited by classes used to clean lexeme rows or flag them to be skipped.
    '''

    #########################################
    def __init__(
        self,
        id_: str,
        description: str,

    ) -> None:
        '''
        Initialiser.

        :param id_: A short unique identifier for the cleaner.
        :param description: A short description of what the cleaner does.
        '''
        self.id_: str = id_
        self.description: str = description

    #########################################
    def clean(
        self,
        row: LexemeRow, # pylint: disable=unused-argument
    ) -> bool:
        '''
        Clean a row using a particular process.

        :param row: A lexeme row to be checked and cleaned.
        :return: Whether the row passes the cleaner's filter.
            A False indicates that it should be skipped.
        '''
        raise NotImplementedError()
