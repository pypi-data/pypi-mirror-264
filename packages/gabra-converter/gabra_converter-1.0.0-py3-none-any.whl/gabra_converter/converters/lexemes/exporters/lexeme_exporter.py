'''
Export lexeme rows to some file format.
'''

from abc import ABC
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow


__all__ = [
    'AddingLexemeRowBeforeFilesCreationException',
    'LexemeExporter'
]


#########################################
class AddingLexemeRowBeforeFilesCreationException(Exception):
    '''
    A LexemesExporter object was used to add a row to a set of files before creating them.
    '''


#########################################
class LexemeExporter(ABC):
    '''
    Abstract class to be inherited by classes used to export lexeme rows into some file format.
    '''

    #########################################
    def __init__(
        self,
        id_: str,
        description: str,
        required_cleaners: set[str],
    ) -> None:
        '''
        Initialiser.

        :param id_: A short unique identifier for the exporter.
        :param description: A short description of what the exporter does.
        :param required_cleaners: A set of lexeme cleaner IDs that this exporter requires in order
            to work.
        '''
        self.id_: str = id_
        self.description: str = description
        self.required_cleaners: set[str] = required_cleaners
        self.id_map: dict[str, int] = {}
        self.out_dir_path: str = ''
        self.__files_created: bool = False

    #########################################
    def get_id_map(
        self,
    ) -> dict[str, int]:
        '''
        Get the lexemes ID map that maps Ġabra lexemes IDs to integer IDs.

        :return: The ID map.
        '''
        return self.id_map

    #########################################
    def create(
        self,
        out_dir_path: str,
    ) -> None:
        '''
        Create a new set of files.
            Must be overriden and called by subclass.

        :param out_dir_path: The directory path to a folder to contain the files.
        '''
        self.id_map = {}
        self.out_dir_path = out_dir_path
        self.__files_created = True

    #########################################
    def add_row(
        self,
        row: LexemeRow, # pylint: disable=unused-argument
    ) -> None:
        '''
        Add a row to the current set of files.
            Must be overriden and called by subclass.

        :param row: A lexeme row to be exported and appended to the files.
        '''
        if not self.__files_created:
            raise AddingLexemeRowBeforeFilesCreationException()
