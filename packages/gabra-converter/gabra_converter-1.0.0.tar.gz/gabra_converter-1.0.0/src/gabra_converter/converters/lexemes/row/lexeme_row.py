'''
A row object for a lexeme from the Ġabra database.

Structure is based on schema in https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema.
'''

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field # pylint: disable=no-name-in-module


__all__ = [
    'POS',
    'Form',
    'Gender',
    'OnomasticType',
    'ExampleType',
    'LexemeRow',
]


#########################################
# Enums
#########################################

#########################################
class POS(Enum):
    '''Part of speech tag enum.'''
    ADJ = 'ADJ'
    ADP = 'ADP'
    ADV = 'ADV'
    AUX = 'AUX'
    CONJ = 'CONJ'
    DET = 'DET'
    INTJ = 'INTJ'
    NOUN = 'NOUN'
    NUM = 'NUM'
    PART = 'PART'
    PRON = 'PRON'
    PROPN = 'PROPN'
    PUNCT = 'PUNCT'
    SCONJ = 'SCONJ'
    SYM = 'SYM'
    VERB = 'VERB'
    X = 'X'


#########################################
class Form(Enum):
    '''General form enum.'''
    MIMATED = 'mimated'
    COMPARATIVE = 'comparative'
    VERBALNOUN = 'verbalnoun'
    DIMINUTIVE = 'diminutive'
    PARTICIPLE = 'participle'
    ACCRETIVE = 'accretive'


#########################################
class Gender(Enum):
    '''Lexeme gender enum.'''
    M = 'm'
    F = 'f'


#########################################
class OnomasticType(Enum):
    '''Onomastic type enum.'''
    TOPONYM = 'toponym'
    ORGANISATION = 'organisation'
    ANTHROPONYM = 'anthroponym'
    COGNOMEN = 'cognomen'
    OTHER = 'other'


#########################################
class ExampleType(Enum):
    '''Example type in gloss objects enum.'''
    FULL = 'full'
    SHORT = 'short'


#########################################
# Pydantic models
#########################################

#########################################
class NumberInt(BaseModel):
    '''Spec for a $numberInt object.'''
    numberInt: int = Field(..., alias='$numberInt')


#########################################
class NumberDouble(BaseModel):
    '''Spec for a $numberDouble object.'''
    numberDouble: int = Field(..., alias='$numberDouble')


#########################################
class Id(BaseModel):
    '''Spec for an $oid object.'''
    oid: str = Field(..., alias='$oid')


#########################################
class Example(BaseModel):
    '''Spec for an example object in a gloss object.'''
    example: str
    type_: Optional[ExampleType] = Field(None, alias='type')


#########################################
class Glosses(BaseModel):
    '''Spec for a glosses object.'''
    gloss: str
    examples: Optional[list[Example]] = None


#########################################
class Root(BaseModel):
    '''Spec for a root object.'''
    radicals: str
    variant: Optional[NumberInt] = None


#########################################
class Headword(BaseModel):
    '''Spec for a headword object.'''
    lemma: str
    pos: Optional[POS] = None


#########################################
class LexemeRow(BaseModel):
    '''A row from the lexemes collection.'''
    id_: Id = Field(..., alias='_id') # The Ġabra unique ID.
    lemma: str # The main lemma.
    alternatives: Optional[list[str]] = None # List of spelling alternatives.
    pos: Optional[POS] = None # Part of speech.
    sources: Optional[list[str]] = None # Source keys.
    glosses: Optional[list[Glosses]] = None # English glosses, with examples.
    root: Optional[Root] = None # Root of entry.
    headword: Optional[Headword] # Headword for entry.
    form: Optional[Form] = None # General form.
    derived_form: Optional[NumberInt] = None # Derived form of verb (1–10).
    gender: Optional[Gender] = None # Male or female.
    transitive: Optional[bool] = None # Transitive verb.
    intransitive: Optional[bool] = None # Intransitive verb.
    ditransitive: Optional[bool] = None # Ditransitive verb.
    hypothetical: Optional[bool] = None # Hypothetical word.
    archaic: Optional[bool] = None # Archaic word.
    multiword: Optional[bool] = None # Multiword expression.
    pending: Optional[bool] = None # Flagged as incorrect or new suggestion.
    phonetic: Optional[str] = None # Phonetic description of lemma.
    apertium_paradigm: Optional[str] = None # Name of paradigm in Apertium lexicon.
    onomastic_type: Optional[OnomasticType] = None # Onomastic type (proper nouns).
    comment: Optional[str] = None # General comment.
