'''
A pipeline that processes JSON encoded wordform rows and exports them.
'''

import json
import pydantic
from gabra_converter.converters.wordforms.row.wordform_row_fixer import fix_wordform_row
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner import WordformCleaner
from gabra_converter.converters.wordforms.exporters.wordform_exporter import WordformExporter
from gabra_converter.converters.wordforms.pipeline.listeners.wordform_pipeline_listener import (
    WordformPipelineListener
)

__all__ = [
    'WordformPipeline',
]


#########################################
class WordformPipeline:
    '''
    The wordform pipeline.
    '''

    #########################################
    def __init__(
        self,
        cleaners: list[WordformCleaner],
        exporter: WordformExporter,
    ) -> None:
        '''
        Initialiser.

        :param cleaners: A list of wordform cleaner objects to sequentially clean a wordform row.
        :param exporter: The wordform exporter object to export a processed row.
        '''
        missing_required_cleaners = (
            exporter.required_cleaners - {cleaner.id_ for cleaner in cleaners}
        )
        if len(missing_required_cleaners) > 0:
            raise ValueError(
                f'The following cleaners are required with exporter {exporter.id_} but were not'
                f' used: {sorted(missing_required_cleaners)}'
            )

        self.out_dir_path: str = ''
        self.cleaners: list[WordformCleaner] = cleaners
        self.exporter: WordformExporter = exporter
        self.listeners: list[WordformPipelineListener] = []

    #########################################
    def add_listener(
        self,
        listener: WordformPipelineListener,
    ) -> None:
        '''
        Add a listener to observe the rows being exported.

        :param listener: The listener.
        '''
        self.listeners.append(listener)

    #########################################
    def create(
        self,
        out_dir_path: str,
    ) -> None:
        '''
        Create a new set of files in which to export together with a 'wordforms_skipped_log.csv'
        file for logging which rows were skipped.

        :param out_dir_path: The directory path to a folder to contain the files.
        '''
        self.exporter.create(out_dir_path)

    #########################################
    def add_row(
        self,
        json_line: str,
        lexemes_id_map: dict[str, int],
    ) -> None:
        '''
        Export another row.

        :param json_line: A line from the extracted wordforms collection.
        :param lexemes_id_map: a dictionary mapping lexeme Ġabra IDs to integer IDs.
            This is returned by a LexemePipeline object.
        '''
        try:
            loaded_json = json.loads(json_line)
        except json.decoder.JSONDecodeError:
            for listener in self.listeners:
                listener.row_skipped(
                    json_line,
                    invalid_json=True,
                    schema_mismatch=False,
                    cleaner=None,
                )
            return

        fix_wordform_row(loaded_json)
        try:
            row = WordformRow(**loaded_json)
        except pydantic.ValidationError:
            for listener in self.listeners:
                listener.row_skipped(
                    json_line,
                    invalid_json=False,
                    schema_mismatch=True,
                    cleaner=None,
                )
            return

        for cleaner in self.cleaners:
            accepted = cleaner.clean(row, lexemes_id_map)
            if not accepted:
                for listener in self.listeners:
                    listener.row_skipped(
                        json_line,
                        invalid_json=False,
                        schema_mismatch=False,
                        cleaner=cleaner,
                    )
                return

        self.exporter.add_row(row, lexemes_id_map)
        for listener in self.listeners:
            listener.row_exported(json_line, row)

    #########################################
    def convert_file(
        self,
        in_file_path: str,
        lexemes_id_map: dict[str, int],
    ) -> None:
        '''
        Convert an entire JSON lines file.

        :param in_file_path: The directory path to an extracted JSON lines collection
            file extracted from Ġabra.
        :param lexemes_id_map: a dictionary mapping lexeme Ġabra IDs to integer IDs.
            This is returned by a LexemePipeline object.
        '''
        with open(in_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line != '\n':
                    self.add_row(line, lexemes_id_map)
