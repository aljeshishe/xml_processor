import logging
from lxml import etree

import random
import string
from pathlib import Path
from zipfile import ZipFile

log = logging.getLogger(__name__)


def random_int():
    return random.randint(1, 100)


def random_string():
    return ''.join(random.choices(string.ascii_letters, k=16))


def create_file():
    '''<root>
    <var name=’id’ value=’<случайное уникальное строковое значение>’/>
    <var name=’level’ value=’<случайное число от 1 до 100>’/>
    <objects><object name=’<случайное строковое значение>’/><object name=’<случайное строковое значение>’/>…</objects></root>'''
    root = etree.Element('root')

    attrib = {'name': 'id', 'value': random_string()}
    etree.SubElement(root, 'var', attrib=attrib)

    attrib = {'name': 'level', 'value': str(random_int())}
    etree.SubElement(root, 'var', attrib=attrib)

    objects = etree.SubElement(root, 'objects')

    objects_count = random.randint(1, 10)
    for i in range(0, objects_count):
        etree.SubElement(objects, 'object', attrib={'name': random_string()})

    return etree.tostring(root, pretty_print=True)


def create(path: Path, archives_count: int = 50, files_count: int = 100):
    log.info(f'Creating {archives_count} zip files with {files_count} files each in {path.absolute()}')
    path.mkdir(exist_ok=False, parents=True)
    for i in range(archives_count):
        file_name = path / f'{i}.zip'
        with ZipFile(file_name, 'w') as fp:
            for j in range(files_count):
                fp.writestr(f'{j}.xml', data=create_file())

