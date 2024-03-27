'''
Export wordform rows to CSV files.
'''

import os
import csv
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.exporters.wordform_exporter import WordformExporter


__all__ = [
    'CSVWordformExporter'
]


#########################################
class CSVWordformExporter(WordformExporter):
    '''
    A concrete WordformExporter class that exports wordforms to comma separated files.
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
            required_cleaners=set(),
        )
        self.__wordform_id: int = 0
        self.__alternative_id: int = 0
        self.__source_id: int = 0

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
        self.__wordform_id = 0
        self.__alternative_id = 0
        self.__source_id = 0

        with open(
            os.path.join(out_dir_path, 'wordforms.csv'),
            'w', encoding='utf-8', newline=''
        ) as wordforms_f, open(
            os.path.join(out_dir_path, 'wordforms_alternatives.csv'),
            'w', encoding='utf-8', newline=''
        ) as alternatives_f, open(
            os.path.join(out_dir_path, 'wordforms_sources.csv'),
            'w', encoding='utf-8', newline=''
        ) as sources_f:
            wordforms_w = csv.writer(wordforms_f)
            alternatives_w = csv.writer(alternatives_f)
            sources_w = csv.writer(sources_f)

            wordforms_w.writerow([
                'new_id',
                'new_lexeme_id',
                '_id',
                'lexeme_id',
                'surface_form',
                'gloss',
                'gender',
                'number',
                'plural_form',
                'subject-person',
                'subject-number',
                'subject-gender',
                'dir_obj-person',
                'dir_obj-number',
                'dir_obj-gender',
                'ind_obj-person',
                'ind_obj-number',
                'ind_obj-gender',
                'possessor-person',
                'possessor-number',
                'possessor-gender',
                'form',
                'aspect',
                'polarity',
                'stem',
                'phonetic',
                'pattern',
                'hypothetical',
                'archaic',
                'generated',
                'pending',
            ])
            alternatives_w.writerow([
                'new_id',
                'new_wordform_id',
                'alternative',
            ])
            sources_w.writerow([
                'new_id',
                'new_wordform_id',
                'source',
            ])

    #########################################
    def add_row(
        self,
        row: WordformRow,
        lexemes_id_map: dict[str, int],
    ) -> None:
        '''
        Add a row to the current set of files.

        :param row: A wordform row to be exported and appended to the files.
        :param lexemes_id_map: a dictionary mapping lexeme Ġabra IDs to integer IDs.
            This is returned by a LexemesExporter object.
        '''
        super().add_row(row, lexemes_id_map)

        with open(
            os.path.join(self.out_dir_path, 'wordforms.csv'),
            'a', encoding='utf-8', newline=''
        ) as wordforms_f, open(
            os.path.join(self.out_dir_path, 'wordforms_alternatives.csv'),
            'a', encoding='utf-8', newline=''
        ) as alternatives_f, open(
            os.path.join(self.out_dir_path, 'wordforms_sources.csv'),
            'a', encoding='utf-8', newline=''
        ) as sources_f:
            wordforms_w = csv.writer(wordforms_f)
            alternatives_w = csv.writer(alternatives_f)
            sources_w = csv.writer(sources_f)

            self.__wordform_id += 1
            wordforms_w.writerow([
                str(self.__wordform_id),
                str(lexemes_id_map.get(row.lexeme_id.oid, '')),
                row.id_.oid,
                row.lexeme_id.oid,
                row.surface_form,
                row.gloss
                    if row.gloss is not None else '',
                row.gender.value
                    if row.gender is not None else '',
                row.number.value
                    if row.number is not None else '',
                row.plural_form
                    if row.plural_form is not None else '',
                row.subject.person.value
                    if row.subject is not None else '',
                row.subject.number.value
                    if row.subject is not None else '',
                row.subject.gender.value
                    if row.subject is not None and row.subject.gender is not None else '',
                row.dir_obj.person.value
                    if row.dir_obj is not None else '',
                row.dir_obj.number.value
                    if row.dir_obj is not None else '',
                row.dir_obj.gender.value
                    if row.dir_obj is not None and row.dir_obj.gender is not None else '',
                row.ind_obj.person.value
                    if row.ind_obj is not None else '',
                row.ind_obj.number.value
                    if row.ind_obj is not None else '',
                row.ind_obj.gender.value
                    if row.ind_obj is not None and row.ind_obj.gender is not None else '',
                row.possessor.person.value
                    if row.possessor is not None else '',
                row.possessor.number.value
                    if row.possessor is not None else '',
                row.possessor.gender.value
                    if row.possessor is not None and row.possessor.gender is not None else '',
                row.form.value
                    if row.form is not None else '',
                row.aspect.value
                    if row.aspect is not None else '',
                row.polarity.value
                    if row.polarity is not None else '',
                row.stem
                    if row.stem is not None else '',
                row.phonetic
                    if row.phonetic is not None else '',
                row.pattern
                    if row.pattern is not None else '',
                ('1' if row.hypothetical else '0')
                    if row.hypothetical is not None else '',
                ('1' if row.archaic else '0')
                    if row.archaic is not None else '',
                ('1' if row.generated else '0')
                    if row.generated is not None else '',
                ('1' if row.pending else '0')
                    if row.pending is not None else '',
            ])

            if row.alternatives is not None:
                for alternative in row.alternatives:
                    self.__alternative_id += 1
                    alternatives_w.writerow([
                        str(self.__alternative_id),
                        str(self.__wordform_id),
                        alternative,
                    ])

            if row.sources is not None:
                for source in row.sources:
                    self.__source_id += 1
                    sources_w.writerow([
                        str(self.__source_id),
                        str(self.__wordform_id),
                        source,
                    ])
