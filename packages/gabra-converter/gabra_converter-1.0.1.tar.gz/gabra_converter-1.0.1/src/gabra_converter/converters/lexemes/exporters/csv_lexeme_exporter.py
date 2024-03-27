'''
Export lexeme rows to CSV files.
'''

import os
import csv
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.exporters.lexeme_exporter import LexemeExporter


__all__ = [
    'CSVLexemeExporter'
]


#########################################
class CSVLexemeExporter(LexemeExporter):
    '''
    A concrete LexemeExporter class that exports lexemes to comma separated files.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__(
            id_='csv',
            description='Export the data into a comma separated file.',
            required_cleaners={'new_lines'},
        )
        self.__lexeme_id: int = 0
        self.__alternative_id: int = 0
        self.__source_id: int = 0
        self.__gloss_id: int = 0
        self.__example_id: int = 0

    #########################################
    def create(
        self,
        out_dir_path: str,
    ) -> None:
        '''
        Create a new set of files.

        :param out_dir_path: The directory path to a folder to contain the files.
        '''
        super().create(out_dir_path)
        self.__lexeme_id = 0
        self.__alternative_id = 0
        self.__source_id = 0
        self.__gloss_id = 0
        self.__example_id = 0

        with open(
            os.path.join(out_dir_path, 'lexemes.csv'),
            'w', encoding='utf-8', newline=''
        ) as lexemes_f, open(
            os.path.join(out_dir_path, 'lexemes_alternatives.csv'),
            'w', encoding='utf-8', newline=''
        ) as alternatives_f, open(
            os.path.join(out_dir_path, 'lexemes_sources.csv'),
            'w', encoding='utf-8', newline=''
        ) as sources_f, open(
            os.path.join(out_dir_path, 'lexemes_glosses.csv'),
            'w', encoding='utf-8', newline=''
        ) as glosses_f, open(
            os.path.join(out_dir_path, 'lexemes_examples.csv'),
            'w', encoding='utf-8', newline=''
        ) as examples_f:
            lexemes_w = csv.writer(lexemes_f)
            alternatives_w = csv.writer(alternatives_f)
            sources_w = csv.writer(sources_f)
            glosses_w = csv.writer(glosses_f)
            examples_w = csv.writer(examples_f)

            lexemes_w.writerow([
                'new_id',
                '_id',
                'lemma',
                'pos',
                'root-radicals',
                'root-variant',
                'headword-lemma',
                'headword-pos',
                'form',
                'derived_form',
                'gender',
                'transitive',
                'intransitive',
                'ditransitive',
                'hypothetical',
                'archaic',
                'multiword',
                'pending',
                'phonetic',
                'apertium_paradigm',
                'onomastic_type',
                'comment',
            ])
            alternatives_w.writerow([
                'new_id',
                'new_lexeme_id',
                'alternative',
            ])
            sources_w.writerow([
                'new_id',
                'new_lexeme_id',
                'source',
            ])
            glosses_w.writerow([
                'new_id',
                'new_lexeme_id',
                'gloss',
            ])
            examples_w.writerow([
                'new_id',
                'new_gloss_id',
                'example',
                'type',
            ])

    #########################################
    def add_row(
        self,
        row: LexemeRow,
    ) -> None:
        '''
        Add a row to the current set of files.

        :param row: A lexeme row to be exported and appended to the files.
        '''
        super().add_row(row)

        with open(
            os.path.join(self.out_dir_path, 'lexemes.csv'),
            'a', encoding='utf-8', newline=''
        ) as lexemes_f, open(
            os.path.join(self.out_dir_path, 'lexemes_alternatives.csv'),
            'a', encoding='utf-8', newline=''
        ) as alternatives_f, open(
            os.path.join(self.out_dir_path, 'lexemes_sources.csv'),
            'a', encoding='utf-8', newline=''
        ) as sources_f, open(
            os.path.join(self.out_dir_path, 'lexemes_glosses.csv'),
            'a', encoding='utf-8', newline=''
        ) as glosses_f, open(
            os.path.join(self.out_dir_path, 'lexemes_examples.csv'),
            'a', encoding='utf-8', newline=''
        ) as examples_f:
            lexemes_w = csv.writer(lexemes_f)
            alternatives_w = csv.writer(alternatives_f)
            sources_w = csv.writer(sources_f)
            glosses_w = csv.writer(glosses_f)
            examples_w = csv.writer(examples_f)

            self.__lexeme_id += 1
            lexemes_w.writerow([
                str(self.__lexeme_id),
                row.id_.oid,
                row.lemma,
                row.pos.value
                    if row.pos is not None else '',
                row.root.radicals
                    if row.root is not None else '',
                str(row.root.variant.numberInt)
                    if row.root is not None and row.root.variant is not None else '',
                row.headword.lemma
                    if row.headword is not None else '',
                row.headword.pos.value
                    if row.headword is not None and row.headword.pos is not None else '',
                row.form.value
                    if row.form is not None else '',
                str(row.derived_form.numberInt)
                    if row.derived_form is not None else '',
                row.gender.value
                    if row.gender is not None else '',
                ('1' if row.transitive else '0')
                    if row.transitive is not None else '',
                ('1' if row.intransitive else '0')
                    if row.intransitive is not None else '',
                ('1' if row.ditransitive else '0')
                    if row.ditransitive is not None else '',
                ('1' if row.hypothetical else '0')
                    if row.hypothetical is not None else '',
                ('1' if row.archaic else '0')
                    if row.archaic is not None else '',
                ('1' if row.multiword else '0')
                    if row.multiword is not None else '',
                ('1' if row.pending else '0')
                    if row.pending is not None else '',
                row.phonetic
                    if row.phonetic is not None else '',
                row.apertium_paradigm
                    if row.apertium_paradigm is not None else '',
                row.onomastic_type.value
                    if row.onomastic_type is not None else '',
                row.comment
                    if row.comment is not None else '',
            ])

            if row.alternatives is not None:
                for alternative in row.alternatives:
                    self.__alternative_id += 1
                    alternatives_w.writerow([
                        str(self.__alternative_id),
                        str(self.__lexeme_id),
                        alternative,
                    ])

            if row.sources is not None:
                for source in row.sources:
                    self.__source_id += 1
                    sources_w.writerow([
                        str(self.__source_id),
                        str(self.__lexeme_id),
                        source,
                    ])

            if row.glosses is not None:
                for gloss in row.glosses:
                    self.__gloss_id += 1
                    glosses_w.writerow([
                        str(self.__gloss_id),
                        str(self.__lexeme_id),
                        gloss.gloss,
                    ])
                    if gloss.examples is not None:
                        for example in gloss.examples:
                            self.__example_id += 1
                            examples_w.writerow([
                                str(self.__example_id),
                                str(self.__gloss_id),
                                example.example,
                                example.type_.value
                                    if example.type_ is not None else '',
                            ])

            self.id_map[row.id_.oid] = self.__lexeme_id
