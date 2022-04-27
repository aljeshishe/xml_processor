import logging
import random
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from zipfile import ZipFile

from lxml import etree

log = logging.getLogger(__name__)


def create_archives(path: Path, archives_count: int = 50, files_count: int = 100) -> None:
    """
    Creates archives with xml files
    :param path: where archives will be places. Created if necessary
    :param archives_count: how much archives will be created
    :param files_count: how much files will be created inside each archive
    """
    log.info(f'Creating {archives_count} zip files with {files_count} files each in {path.absolute()}')
    path.mkdir(exist_ok=False, parents=True)
    with ProcessPoolExecutor() as pool:
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

    attrib = {'name': 'id', 'value': str(uuid.uuid4())}
    etree.SubElement(root, 'var', attrib=attrib)

    attrib = {'name': 'level', 'value': str(random.randint(1, 100))}
    etree.SubElement(root, 'var', attrib=attrib)

    objects = etree.SubElement(root, 'objects')

    objects_count = random.randint(1, 10)
    for i in range(0, objects_count):
        etree.SubElement(objects, 'object', attrib={'name': str(uuid.uuid4())})

    return etree.tostring(root, pretty_print=True)


