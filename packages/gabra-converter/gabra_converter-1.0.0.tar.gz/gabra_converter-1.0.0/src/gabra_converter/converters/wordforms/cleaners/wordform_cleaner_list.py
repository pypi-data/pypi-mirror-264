'''
A list of available wordform cleaners.
'''

from gabra_converter.converters.wordforms.cleaners.wordform_cleaner import WordformCleaner
from gabra_converter.converters.wordforms.cleaners.missing_lexeme_wordform_cleaner import (
    MissingLexemeWordformCleaner
)
from gabra_converter.converters.wordforms.cleaners.surfaceform_spaces_wordform_cleaner import (
    SurfaceformSpacesWordformCleaner
)
from gabra_converter.converters.wordforms.cleaners.surfaceform_capitals_wordform_cleaner import (
    SurfaceformCapitalsWordformCleaner
)
from gabra_converter.converters.wordforms.cleaners.surfaceform_nonmaltese_wordform_cleaner import (
    SurfaceformNonmalteseWordformCleaner
)
from gabra_converter.converters.wordforms.cleaners.pending_wordform_cleaner import (
    PendingWordformCleaner
)


__all__ = [
    'get_all_wordform_cleaners',
]


#########################################
__all_wordform_cleaners: list[WordformCleaner] = [
    MissingLexemeWordformCleaner(),
    SurfaceformSpacesWordformCleaner(),
    SurfaceformCapitalsWordformCleaner(),
    SurfaceformNonmalteseWordformCleaner(),
    PendingWordformCleaner(),

]
def get_all_wordform_cleaners(
) -> list[WordformCleaner]:
    '''
    Get a list of all the available wordform cleaners.

    :return: The list.
    '''
    return __all_wordform_cleaners
