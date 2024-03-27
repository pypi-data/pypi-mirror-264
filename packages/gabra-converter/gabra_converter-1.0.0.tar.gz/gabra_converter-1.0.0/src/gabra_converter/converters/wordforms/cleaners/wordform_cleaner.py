'''
Clean or flag for skipping a wordform row based on some condition.
'''

from abc import ABC
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow


__all__ = [
    'WordformCleaner',
]


#########################################
class WordformCleaner(ABC):
    '''
    Abstract class to be inherited by classes used to clean wordform rows or flag them to be
    skipped.
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
        raise NotImplementedError()
