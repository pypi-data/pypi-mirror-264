'''
Export wordform rows to some file format.
'''

from abc import ABC
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow


__all__ = [
    'AddingWordformRowBeforeFilesCreationException',
    'WordformExporter'
]


#########################################
class AddingWordformRowBeforeFilesCreationException(Exception):
    '''
    A WordformsExporter object was used to add a row to a set of files before creating them.
    '''


#########################################
class WordformExporter(ABC):
    '''
    Abstract class to be inherited by classes used to export wordform rows into some file format.
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
        :param required_cleaners: A set of wordform cleaner IDs that this exporter requires in order
            to work.
        '''
        self.id_: str = id_
        self.description: str = description
        self.required_cleaners: set[str] = required_cleaners
        self.out_dir_path: str = ''
        self.__files_created: bool = False

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
        self.out_dir_path = out_dir_path
        self.__files_created = True

    #########################################
    def add_row(
        self,
        row: WordformRow, # pylint: disable=unused-argument
        lexemes_id_map: dict[str, int], # pylint: disable=unused-argument
    ) -> None:
        '''
        Add a row to the current set of files.
            Must be overriden and called by subclass.

        :param row: A wordform row to be exported and appended to the files.
        :param lexemes_id_map: a dictionary mapping lexeme Ġabra IDs to integer IDs.
            This is returned by a LexemesExporter object.
        '''
        if not self.__files_created:
            raise AddingWordformRowBeforeFilesCreationException()
