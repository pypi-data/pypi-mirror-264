'''
Code for fixing known wordform rows in the Ġabra database that do not match the specification.

Specification is from schema in https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema.
'''

from typing import Any


__all__ = [
    'fix_wordform_row',
]


#########################################
def _fix_alternatives_not_list(
    row: dict[str, Any],
) -> None:
    '''
    Fix alternatives field that is a string instead of a list by putting the string in a list.

    :param row: A row from the wordforms collection.
    '''
    if 'alternatives' in row and isinstance(row['alternatives'], str):
        row['alternatives'] = [row['alternatives']]


#########################################
def _fix_empty_number(
    row: dict[str, Any],
) -> None:
    '''
    Fix number field that is an empty string by removing the number field.

    :param row: A row from the wordforms collection.
    '''
    if 'number' in row and row['number'] == '':
        del row['number']


#########################################
def fix_wordform_row(
    row: dict[str, Any],
) -> dict[str, Any]:
    '''
    Fix rows in the wordform collection that are known to diverge from the specification.

    :param row: A row from the wordforms collection.
    :return: A reference to ``row``.
    '''
    _fix_alternatives_not_list(row)
    _fix_empty_number(row)
    return row
