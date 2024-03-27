'''
A pipeline that completely processes a Ġabra database dump and exports it from start to finish.
'''

import os
import tempfile
from abc import ABC
from gabra_converter.converters.archive_extractor import extract_archived_files, convert_bson_file
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner
from gabra_converter.converters.lexemes.exporters.lexeme_exporter import LexemeExporter
from gabra_converter.converters.lexemes.pipeline.lexeme_pipeline import LexemePipeline
from gabra_converter.converters.lexemes.pipeline.listeners.lexeme_pipeline_listener \
    import LexemePipelineListener
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner import WordformCleaner
from gabra_converter.converters.wordforms.exporters.wordform_exporter import WordformExporter
from gabra_converter.converters.wordforms.pipeline.wordform_pipeline import WordformPipeline
from gabra_converter.converters.wordforms.pipeline.listeners.wordform_pipeline_listener \
    import WordformPipelineListener


__all__ = [
    'PipelineListener',
    'pipeline',
]


#########################################
class PipelineListener(ABC):
    '''
    Abstract class to be inherited by pipeline listeners.
    Listens to the different high level stages in the pipeline process.
    In order, the stages are:

    - started_extracting
    - ended_extracting
    - started_converting_lexemes
    - ended_converting_lexemes
    - started_converting_wordforms
    - ended_converting_wordforms
    - started_exporting_lexemes
    - ended_exporting_lexemes
    - started_exporting_wordforms
    - ended_exporting_wordforms

    An explanation of each stage is given in the listener methods below.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''

    #########################################
    def started_extracting(
        self,
    ) -> None:
        '''
        Listen for when the compressed database dump started being extracted into BSON files.
        '''

    #########################################
    def ended_extracting(
        self,
    ) -> None:
        '''
        Listen for when the compressed database dump stopped being extracted into BSON files.
        '''

    #########################################
    def started_converting_lexemes(
        self,
    ) -> None:
        '''
        Listen for when the lexemes BSON file started being converted into a JSONL file.
        '''

    #########################################
    def ended_converting_lexemes(
        self,
    ) -> None:
        '''
        Listen for when the lexemes BSON file stopped being converted into a JSONL file.
        '''

    #########################################
    def started_converting_wordforms(
        self,
    ) -> None:
        '''
        Listen for when the wordforms BSON file started being converted into a JSONL file.
        '''

    #########################################
    def ended_converting_wordforms(
        self,
    ) -> None:
        '''
        Listen for when the wordforms BSON file stopped being converted into a JSONL file.
        '''

    #########################################
    def started_exporting_lexemes(
        self,
    ) -> None:
        '''
        Listen for when the lexemes JSONL file started being exported into the target format.
        '''

    #########################################
    def ended_exporting_lexemes(
        self,
    ) -> None:
        '''
        Listen for when the lexemes JSONL file stopped being exported into the target format.
        '''

    #########################################
    def started_exporting_wordforms(
        self,
    ) -> None:
        '''
        Listen for when the wordforms JSONL file started being exported into the target format.
        '''

    #########################################
    def ended_exporting_wordforms(
        self,
    ) -> None:
        '''
        Listen for when the wordforms JSONL file stopped being exported into the target format.
        '''


#########################################
def pipeline(
    gabra_dump_path: str,
    out_path: str,
    lexeme_cleaners: list[LexemeCleaner],
    wordform_cleaners: list[WordformCleaner],
    lexeme_exporter: LexemeExporter,
    wordform_exporter: WordformExporter,
    lexeme_pipeline_listeners: list[LexemePipelineListener],
    wordform_pipeline_listeners: list[WordformPipelineListener],
    pipeline_listeners: list[PipelineListener],
) -> None:
    '''
    Export the data in a Ġabra dump file from start to finish.

    :param gabra_dump_path: The path to the .tar.gz Ġabra dump file downloaded from the website.
    :param out_path: The path to a folder that will contain the output files.
        The path will be created if it doesn't exist.
    :param lexeme_cleaners: A list of cleaners to apply to the lexemes.
    :param wordform_cleaners: A list of cleaners to apply to the wordforms.
    :param lexeme_exporter: The lexeme exporter to use.
    :param wordform_exporter: The wordform exporter to use.
    :param lexeme_pipeline_listeners: A list of listeners for each lexeme exported.
    :param wordform_pipeline_listeners: A list of listeners for each wordform exported.
    :param pipeline_listeners: A list of listeners for the different high level pipeline stages.
    '''
    with tempfile.TemporaryDirectory() as tmp_path:
        for listener in pipeline_listeners:
            listener.started_extracting()
        extract_archived_files(gabra_dump_path, tmp_path)
        for listener in pipeline_listeners:
            listener.ended_extracting()

        for listener in pipeline_listeners:
            listener.started_converting_lexemes()
        convert_bson_file(
            os.path.join(tmp_path, 'tmp', 'gabra', 'lexemes.bson'),
            os.path.join(tmp_path, 'lexemes.jsonl'),
        )
        for listener in pipeline_listeners:
            listener.ended_converting_lexemes()

        for listener in pipeline_listeners:
            listener.started_converting_wordforms()
        convert_bson_file(
            os.path.join(tmp_path, 'tmp', 'gabra', 'wordforms.bson'),
            os.path.join(tmp_path, 'wordforms.jsonl'),
        )
        for listener in pipeline_listeners:
            listener.ended_converting_wordforms()

        os.makedirs(out_path, exist_ok=True)

        for listener in pipeline_listeners:
            listener.started_exporting_lexemes()
        lexeme_pipeline = LexemePipeline(lexeme_cleaners, lexeme_exporter)
        for lexeme_listener in lexeme_pipeline_listeners:
            lexeme_pipeline.add_listener(lexeme_listener)
        lexeme_pipeline.create(out_path)
        lexeme_pipeline.convert_file(os.path.join(tmp_path, 'lexemes.jsonl'))
        lexeme_ids = lexeme_pipeline.get_id_map()
        for listener in pipeline_listeners:
            listener.ended_exporting_lexemes()

        for listener in pipeline_listeners:
            listener.started_exporting_wordforms()
        wordform_pipeline = WordformPipeline(wordform_cleaners, wordform_exporter)
        for wordform_listener in wordform_pipeline_listeners:
            wordform_pipeline.add_listener(wordform_listener)
        wordform_pipeline.create(out_path)
        wordform_pipeline.convert_file(os.path.join(tmp_path, 'wordforms.jsonl'), lexeme_ids)
        for listener in pipeline_listeners:
            listener.ended_exporting_wordforms()
