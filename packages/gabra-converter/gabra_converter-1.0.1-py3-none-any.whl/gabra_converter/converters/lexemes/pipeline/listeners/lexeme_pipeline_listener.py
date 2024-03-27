'''
Listen for events while a lexeme pipeline is in progress.
'''

from abc import ABC
from typing import Optional
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow

__all__ = [
    'LexemePipelineListener',
]

#########################################
class LexemePipelineListener(ABC):
    '''
    Abstract class to be inherited by lexeme pipeline listeners.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''

    #########################################
    def row_exported(
        self,
        json_line: str,
        row: LexemeRow,
    ) -> None:
        '''
        Listen for when a row is successfully exported.

        :param json_line: The raw JSON line that was processed.
        :param row: The processed row that was exported.
        '''

    #########################################
    def row_skipped(
        self,
        json_line: str, # pylint: disable=unused-argument
        invalid_json: bool,
        schema_mismatch: bool,
        cleaner: Optional[LexemeCleaner],
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
        if (cleaner is not None) == (invalid_json or schema_mismatch):
            raise ValueError(
                'If the JSON was invalid or did not match the schema then a cleaner could not'
                ' have been used whilst if a cleaner was used then the JSON was both valid and'
                ' matched the schema. Therefore, cleaner must be None when invalid_json or '
                ' schema mismatch is true and vice versa.'
            )
        if invalid_json and schema_mismatch:
            raise ValueError(
                'If the JSON was invalid then it cannot have been compared to the schema and if'
                ' it was compared to the schema then it was valid. Therefore, invalid_json and'
                ' schema mismatch cannot be both true.'
            )
