'''
A list of available wordform exporters.
'''

from gabra_converter.converters.wordforms.exporters.wordform_exporter import WordformExporter
from gabra_converter.converters.wordforms.exporters.csv_wordform_exporter import CSVWordformExporter


__all__ = [
    'get_all_wordform_exporters',
]


#########################################
__all_wordform_exporters: list[WordformExporter] = [
    CSVWordformExporter(),
]
def get_all_wordform_exporters(
) -> list[WordformExporter]:
    '''
    Get a list of all the available wordform exporters.

    :return: The list.
    '''
    return __all_wordform_exporters
