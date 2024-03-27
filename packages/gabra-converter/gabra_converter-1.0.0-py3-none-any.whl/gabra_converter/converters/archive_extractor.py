'''
Database dump extraction code.
'''

import subprocess


__all__ = [
    'extract_archived_files',
    'convert_bson_file',
]


#########################################
def extract_archived_files(
    archive_path: str,
    dest_path: str,
) -> None:
    '''
    Extract the archived files.

    :param archive_path: The path to the archive to extract from.
    :param dest_path: The destination path where to store the extracted data.
    '''
    subprocess.run([
        'tar', '-zxvf',
        archive_path,
        '-C', dest_path,
    ], check=True)


#########################################
def convert_bson_file(
    bson_path: str,
    dest_path: str,
) -> None:
    '''
    Convert a BSON file into a JSON lines file.

    :param bson_path: The path to the BSON file.
    :param dest_path: The path to the extracted JSON lines file.
    '''
    subprocess.run([
        'bsondump',
        bson_path,
        f'--outFile={dest_path}'
    ], check=True)
