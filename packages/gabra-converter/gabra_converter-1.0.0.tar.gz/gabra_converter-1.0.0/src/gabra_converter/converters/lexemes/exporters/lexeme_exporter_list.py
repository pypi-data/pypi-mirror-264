'''
A list of available lexeme exporters.
'''

from gabra_converter.converters.lexemes.exporters.lexeme_exporter import LexemeExporter
from gabra_converter.converters.lexemes.exporters.csv_lexeme_exporter import CSVLexemeExporter


__all__ = [
    'get_all_lexeme_exporters',
]


#########################################
__all_lexeme_exporters: list[LexemeExporter] = [
    CSVLexemeExporter(),
]
def get_all_lexeme_exporters(
) -> list[LexemeExporter]:
    '''
    Get a list of all the available lexeme exporters.

    :return: The list.
    '''
    return __all_lexeme_exporters
