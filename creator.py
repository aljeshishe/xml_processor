import logging
import random
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from typing import Optional

log = logging.getLogger(__name__)


def create_archives(path: Path, archives_count: int = 50, files_count: int = 100, workers: Optional[int] = None) -> None:
    """
    Creates archives with xml files
    :param path: where archives will be places. Created if necessary
    :param archives_count: how much archives will be created
    :param files_count: how much files will be created inside each archive
    :param workers: how much workers to use
    """
    log.info(f'Creating {archives_count} zip files with {files_count} files each in {path.absolute()}')
    path.mkdir(exist_ok=True, parents=True)
    with ProcessPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_create_archive,
                               path=path / f'{i}.zip',
                               files_count=files_count)
                   for i in range(archives_count)]

        # check results in case of exceptions
        for future in as_completed(futures):
            future.result()


def _create_archive(path: Path, files_count: int):
    """
    Created archive with xml files
    """
    with ZipFile(path, 'w') as fp:
        for i in range(files_count):
            fp.writestr(f'{i}.xml', data=_create_content())


def _new_id():
    return str(uuid.uuid4())


def _new_level():
    return str(random.randint(1, 100))


def _new_object_name():
    return str(uuid.uuid4())


def _objects_count():
    return random.randint(1, 10)


def _create_content() -> str:
    """
    Returns xml file content with following structure
    <root>
        <var name=’id’ value=’<случайное уникальное строковое значение>’/>
        <var name=’level’ value=’<случайное число от 1 до 100>’/>
        <objects>
            <object name=’<случайное строковое значение>’/>
            <object name=’<случайное строковое значение>’/
        </objects>
    </root>
    """
    root = etree.Element('root')

    attrib = {'name': 'id', 'value': _new_id()}
    etree.SubElement(root, 'var', attrib=attrib)

    attrib = {'name': 'level', 'value': _new_level()}
    etree.SubElement(root, 'var', attrib=attrib)

    objects = etree.SubElement(root, 'objects')

    objects_count = _objects_count()
    for i in range(0, objects_count):
        etree.SubElement(objects, 'object', attrib={'name': _new_object_name()})

    content = etree.tostring(root, pretty_print=True)
    return content


