# Ġabra Converter

This program converts [Ġabra](https://mlrs.research.um.edu.mt/resources/gabra/)'s [database dump files](https://mlrs.research.um.edu.mt/resources/gabra-api/p/download), which are for [MongoDB](https://www.mongodb.com/), into a more accessible format, as well as cleaning and normalising it.

## How to use

To use this program, you will need to have the following command line commands available on your computer:

- `tar`: [7-zip archiver](https://www.7-zip.org/download.html)
- `bsondump`: [MongoDB tool](https://www.mongodb.com/docs/database-tools/installation/installation/)

Make sure that you install the above applications and then test them in your command line with the following commands:

- `tar --version`
- `bsondump --version`

Once you have these applications available in your command line, you can now download a [Ġabra database dump file](https://mlrs.research.um.edu.mt/resources/gabra-api/p/download).

Use the exporter by calling `python bin/run_gabra_converter.py` or `gabra_converter.exe` in the command line as follows:

`python bin/run_gabra_converter.py --gabra_dump_path <path to dump file> --out_path <path to folder with exported files> --lexeme_cleaners <space separated list of lexeme cleaner names> --wordform_cleaners <space separated list of wordform cleaner names> --lexeme_exporter <exporter name> --wordform_exporter <exporter name, usually the same as the lexeme exporter>`

Here is a typical example:

`python bin/run_gabra_converter.py --gabra_dump_path path/to/gabra --out_path path/to/out --lexeme_cleaners new_lines --wordform_cleaners --lexeme_exporter csv --wordform_exporter csv`

or with the `gabra_converter.exe`:

`gabra_converter --gabra_dump_path path/to/gabra --out_path path/to/out --lexeme_cleaners new_lines --wordform_cleaners --lexeme_exporter csv --wordform_exporter csv`

Run `python bin/run_gabra_converter.py --help` or `gabra_converter --help` for more information.

## What is exported

All the exported data is based on [the official Ġabra schema](https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema).
Whilst MongoDB is a NoSQL database which allows for leaving fields out completely in database rows (note that rows are called documents and tables are called collections in MongoDB), the exported data is structured as flat tables.
All the fields in the schema are used in the export and left empty if unused in a row.
On the other hand, any fields that are not mentioned in the schema but still used in the rows, such as `norm_freq`, are left out.

A number of files are generated to handle one-to-many relationships.
For example, since one lexeme can have many glosses (glosses are stored as a list in Ġabra), a separate file for glosses is created such that each row in the lexemes file can refer to multiple rows in the glosses file.
Non-list fields that are represented as nested objects are flattened such that the field `"root":{"radicals":"b-ħ-b-ħ","variant":2}"` becomes two fields: `root-radicals` and `root-variant`, with the dash used to separate parent names from child names.
Any unnecessarily nested objects produced by MongoDB that are used to specify data types (objects consisting of just one field with a dollar sign at the front of the field name) are not preserved.
So numbers being stored in `"$numberInt"` such as `"derived_form":{"$numberInt":1}` will be exported as `derived_form` without reference to the nested object.
Boolean values are represented as 0 for false and 1 for true.
Finally, while MongoDB uses hexadecimal numbers for primary and foreign keys, such as 63b1e0f314e849fa182bcfc3, the export also includes its own decimal primary and foreign keys for ease of use in relational databases.
These fields will have their field names prefixed with `new_`, such as `new_id` and `new_lexeme_id`.

The following exporters are supported:

### `csv`

At the moment, the program only supports CSV (Comma Separated Values) file exports.
The files generated are the following:

- `lexemes.csv`: Contains all the non-list fields in the lexemes collection.
    Includes a decimal unique ID `new_id` field and the original hexadecimal unique ID `_id` field.
- `lexemes_alternatives.csv`: Contains the alternative words of each lexeme on separate rows using the `new_lexeme_id` field to link to the lexeme's `new_id` field.
    Includes a decimal unique ID `new_id`.
- `lexemes_sources.csv`: Contains the [sources](https://mlrs.research.um.edu.mt/resources/gabra/sources) of each lexeme on separate rows using the `new_lexeme_id` field to link to the lexeme's `new_id` field.
    Includes a decimal unique ID `new_id`.
- `lexemes_glosses.csv`: Contains the different glosses (definitions in English) of each lexeme on separate rows using the `new_lexeme_id` field to link to the lexeme's `new_id` field.
    Includes a decimal unique ID `new_id`.
- `lexemes_examples.csv`: Contains the different examples of each lexeme's gloss on separate rows using the `new_gloss_id` field to link to the gloss's `new_id` field.
    Includes a decimal unique ID `new_id`.
- `wordforms.csv`: Contains all the non-list fields in the wordforms collection.
    Includes a decimal unique ID `new_id` field, a decimal lexeme ID reference called `new_lexeme_id`, and the original hexadecimal unique ID `_id` field.
- `wordforms_alternatives.csv`: Contains the alternative words of each wordform on separate rows using the `new_wordform_id` field to link to the wordform's `new_id` field.
    Includes a decimal unique ID `new_id`.
- `wordforms_sources.csv`: Contains the [sources](https://mlrs.research.um.edu.mt/resources/gabra/sources) of each wordform on separate rows using the `new_wordform_id` field to link to the wordform's `new_id` field.
    Includes a decimal unique ID `new_id`.

## Available cleaners

There are a number of options available for skipping or cleaning certain rows from the Ġabra database.
Some are required whilst others are optional, depending on the exporter used.

### Lexeme related cleaners

- `new_lines`: Remove new lines from the glosses and examples of lexemes.
- `lemma_capitals`: Skip any lexemes whose lemma contains uppercase letters.
- `lemma_nonmaltese`: Skip any lexemes whose lemma contains non-Maltese letters.
- `lemma_spaces`: Skip any lexemes whose lemma contains spaces.
- `pending`: Skip any lexemes whose pending field is not set to false.

Required cleaners:

||`csv`|
|---|---|
|`new_lines`|required|
|`lemma_capitals`||
|`lemma_nonmaltese`||
|`lemma_spaced`||
|`pending`||

### Wordform related cleaners

- `missing_lexeme`: Skip any wordforms whose lexeme ID does not refer to an existing lexeme.
- `surfaceform_capitals`: Skip any wordforms whose surfaceform contains uppercase letters.
- `surfaceform_nonmaltese`: Skip any wordforms whose surfaceform contains non-Maltese letters.
- `surfaceform_spaces`: Skip any wordforms whose surfaceform contains spaces.
- `pending`: Skip any wordforms whose pending field is not set to false.

Required cleaners:

||`csv`|
|---|---|
|`missing_lexeme`||
|`surfaceform_capitals`||
|`surfaceform_nonmaltese`||
|`surfaceform_spaces`||
|`pending`||
