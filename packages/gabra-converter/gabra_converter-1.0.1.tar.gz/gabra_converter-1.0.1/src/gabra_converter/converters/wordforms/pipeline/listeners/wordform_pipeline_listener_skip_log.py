'''
Keep a log of all the wordforms that were skipped in a tab separated values file.
'''

import os
from typing import Optional
from gabra_converter.converters.wordforms.pipeline.listeners.wordform_pipeline_listener import (
    WordformPipelineListener
)
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner import WordformCleaner

__all__ = [
    'WordformPipelineListener',
    'LoggingWordformSkipBeforeFileCreationException',
]


#########################################
class LoggingWordformSkipBeforeFileCreationException(Exception):
    '''
    A WordformPipelineListeneSkipLog object was used to log a skipped row before creating the log
    file.
    '''


#########################################
class WordformPipelineListenerSkipLog(WordformPipelineListener):
    '''
    Log all the wordforms that were skipped.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__()
        self.out_dir_path: str = ''
        self.__files_created: bool = False

    #########################################
    def create(
        self,
        out_dir_path: str,
    ) -> None:
        '''
        Create a new set of files.

        :param out_dir_path: The directory path to a folder to contain the files.
        '''
        with open(
            os.path.join(out_dir_path, 'wordforms_skipped_log.txt'),
            'w', encoding='utf-8', newline=''
        ) as skipped_f:
            print('json_line', 'reason', sep='\t', file=skipped_f)
        self.out_dir_path = out_dir_path
        self.__files_created = True

    #########################################
    def row_skipped(
        self,
        json_line: str,
        invalid_json: bool,
        schema_mismatch: bool,
        cleaner: Optional[WordformCleaner],
    ) -> None:
        '''
        Listen for when a row was skipped.

        :param json_line: The verbatim JSON row that was skipped.
        :param invalid_json: Whether the JSON row was not in valid JSON format.
        :param schema_mismatch: Whether the JSON row did not conform to the Ġabra schema.
        :param cleaner: The cleaner that determined that the row should be skipped.
            If None, then the reason is that it was either not valid JSON or did not conform
            to the Ġabra schema.

        invalid_json and schema_mismatch cannot both be true and if one of them is true then
        cleaner cannot be set. If cleaner is set then both invalid_json and schema_mismatch
        must be false.
        '''
        super().row_skipped(json_line, invalid_json, schema_mismatch, cleaner)

        if not self.__files_created:
            raise LoggingWordformSkipBeforeFileCreationException()

        if cleaner is None:
            if invalid_json:
                reason = 'Invalid JSON'
            elif schema_mismatch:
                reason = 'Schema mismatch'
        else:
            reason = cleaner.id_

        with open(
            os.path.join(self.out_dir_path, 'wordforms_skipped_log.txt'),
            'a', encoding='utf-8', newline=''
        ) as skipped_f:
            print(json_line.strip(), reason, sep='\t', file=skipped_f)
