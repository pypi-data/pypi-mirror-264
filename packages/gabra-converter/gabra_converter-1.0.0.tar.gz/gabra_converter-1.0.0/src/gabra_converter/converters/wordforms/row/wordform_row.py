'''
A row object for a wordform from the Ġabra database.

Structure is based on schema in https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema.
'''

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field # pylint: disable=no-name-in-module


__all__ = [
    'Person',
    'Gender',
    'Number',
    'Form',
    'Aspect',
    'Polarity',
    'WordformRow',
]


#########################################
# Enums
#########################################

#########################################
class Person(Enum):
    '''Grammatical person enum.'''
    P1 = 'p1'
    P2 = 'p2'
    P3 = 'p3'


#########################################
class Gender(Enum):
    '''Grammatical gender enum.'''
    M = 'm'
    F = 'f'
    MF = 'mf'


#########################################
class Number(Enum):
    '''Grammatical number enum.'''
    SG = 'sg'
    DL = 'dl'
    PL = 'pl'
    SGV = 'sgv'
    COLL = 'coll'
    SP = 'sp'
    PL_IND = 'pl_ind'
    PL_DET = 'pl_det'
    PL_PL = 'pl_pl'


#########################################
class Form(Enum):
    '''General form enum.'''
    COMPARATIVE = 'comparative'
    SUPERLATIVE = 'superlative'
    DIMINUTIVE = 'diminutive'
    INTERROGATIVE = 'interrogative'
    MIMATED = 'mimated'
    VERBALNOUN = 'verbalnoun'


#########################################
class Aspect(Enum):
    '''General form enum.'''
    PERF = 'perf'
    IMPF = 'impf'
    IMP = 'imp'
    PASTPART = 'pastpart'
    PRESPART = 'prespart'


#########################################
class Polarity(Enum):
    '''Positive/negative enum.'''
    POS = 'pos'
    NEG = 'neg'


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
class Grammeme(BaseModel):
    '''Spec for a grammeme object.'''
    person: Person
    number: Number
    gender: Optional[Gender]


#########################################
class WordformRow(BaseModel):
    '''A row from the wordforms collection.'''
    id_: Id = Field(..., alias='_id') # The Ġabra unique ID.
    lexeme_id: Id # Should be a valid ID in lexemes collection.
    surface_form: str # Surface form.
    alternatives: Optional[list[str]] = None # List of spelling alternatives.
    gloss: Optional[str] = None # English gloss.
    sources: Optional[list[str]] = None # Source keys.
    gender: Optional[Gender] = None # Male, female, male-female.
    number: Optional[Number] = None # Number.
    plural_form: Optional[str] = None # Plural type.
    subject: Optional[Grammeme] = None # Subject agreement (verbs).
    dir_obj: Optional[Grammeme] = None # Direct object agreement.
    ind_obj: Optional[Grammeme] = None # Indirect object agreement.
    possessor: Optional[Grammeme] = None # Agreement for nouns which inflect for possessive.
    form: Optional[Form] = None # General morphological form.
    aspect: Optional[Aspect] = None # Aspect (verbs).
    polarity: Optional[Polarity] = None # Polarity.
    stem: Optional[str] = None # Stem.
    phonetic: Optional[str] = None # Phonetic transcription.
    pattern: Optional[str] = None # Vowel-consonant pattern.
    hypothetical: Optional[bool] = None # Hypothetical.
    archaic: Optional[bool] = None # Archaic.
    generated: Optional[bool] = None # Generated.
    pending: Optional[bool] = None # Flagged as incorrect or new suggestion
