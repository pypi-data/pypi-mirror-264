'''
A pipeline that processes JSON encoded lexeme rows and exports them.
'''

import json
import pydantic
from gabra_converter.converters.lexemes.row.lexeme_row_fixer import fix_lexeme_row
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner
from gabra_converter.converters.lexemes.exporters.lexeme_exporter import LexemeExporter
from gabra_converter.converters.lexemes.pipeline.listeners.lexeme_pipeline_listener import (
    LexemePipelineListener
)


#########################################
class LexemePipeline:
    '''
    The lexeme pipeline.
    '''

    #########################################
    def __init__(
        self,
        cleaners: list[LexemeCleaner],
        exporter: LexemeExporter,
    ) -> None:
        '''
        Initialiser.

        :param cleaners: A list of lexeme cleaner objects to sequentially clean a lexeme row.
        :param exporter: The lexeme exporter object to export a processed row.
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
        self.cleaners: list[LexemeCleaner] = cleaners
        self.exporter: LexemeExporter = exporter
        self.listeners: list[LexemePipelineListener] = []

    #########################################
    def add_listener(
        self,
        listener: LexemePipelineListener,
    ) -> None:
        '''
        Add a listener to observe the rows being exported.

        :param listener: The listener.
        '''
        self.listeners.append(listener)

    #########################################
    def get_id_map(
        self,
    ) -> dict[str, int]:
        '''
        Get the lexemes ID map that maps Ġabra lexemes IDs to integer IDs.

        :return: The ID map.
        '''
        return self.exporter.id_map

    #########################################
    def create(
        self,
        out_dir_path: str,
    ) -> None:
        '''
        Create a new set of files in which to export together with a 'lexemes_skipped_log.csv'
        file for logging which rows were skipped.

        :param out_dir_path: The directory path to a folder to contain the files.
        '''
        self.exporter.create(out_dir_path)

    #########################################
    def add_row(
        self,
        json_line: str,
    ) -> None:
        '''
        Export another row.

        :param json_line: A line from the extracted lexemes collection.
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

        fix_lexeme_row(loaded_json)

        try:
            row = LexemeRow(**loaded_json)
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
            accepted = cleaner.clean(row)
            if not accepted:
                for listener in self.listeners:
                    listener.row_skipped(
                        json_line,
                        invalid_json=False,
                        schema_mismatch=False,
                        cleaner=cleaner,
                    )
                return

        self.exporter.add_row(row)
        for listener in self.listeners:
            listener.row_exported(json_line, row)

    #########################################
    def convert_file(
        self,
        in_file_path: str,
    ) -> None:
        '''
        Convert an entire JSON lines file.

        :param in_file_path: The directory path to an extracted JSON lines collection
            file extracted from Ġabra.
        '''
        with open(in_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line != '\n':
                    self.add_row(line)
