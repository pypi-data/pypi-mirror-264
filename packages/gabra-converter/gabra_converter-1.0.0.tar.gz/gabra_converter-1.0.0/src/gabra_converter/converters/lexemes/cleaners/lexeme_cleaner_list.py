'''
A list of available lexeme cleaners.
'''

from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner import LexemeCleaner
from gabra_converter.converters.lexemes.cleaners.new_lines_lexeme_cleaner import (
    NewLinesLexemeCleaner
)
from gabra_converter.converters.lexemes.cleaners.lemma_spaces_lexeme_cleaner import (
    LemmaSpacesLexemeCleaner
)
from gabra_converter.converters.lexemes.cleaners.lemma_capitals_lexeme_cleaner import (
    LemmaCapitalsLexemeCleaner
)
from gabra_converter.converters.lexemes.cleaners.lemma_nonmaltese_lexeme_cleaner import (
    LemmaNonmalteseLexemeCleaner
)
from gabra_converter.converters.lexemes.cleaners.pending_lexeme_cleaner import (
    PendingLexemeCleaner
)


__all__ = [
    'get_all_lexeme_cleaners',
]


#########################################
__all_lexeme_cleaners: list[LexemeCleaner] = [
    NewLinesLexemeCleaner(),
    LemmaSpacesLexemeCleaner(),
    LemmaCapitalsLexemeCleaner(),
    LemmaNonmalteseLexemeCleaner(),
    PendingLexemeCleaner(),

]
def get_all_lexeme_cleaners(
) -> list[LexemeCleaner]:
    '''
    Get a list of all the available lexeme cleaners.

    :return: The list.
    '''
    return __all_lexeme_cleaners
