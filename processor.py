from result import Result
from typing import Iterable

import logging
from concurrent.futures.process import ProcessPoolExecutor
from lxml import etree
from pathlib import Path

from zipfile import ZipFile

log = logging.getLogger(__name__)


def process_file(path: Path) -> Result:
    with ZipFile(path) as fp:
        results = []
        for name in fp.namelist():
            tree = etree.fromstring(fp.read(name))
            result = Result(id=tree.find('var[@name="id"]').attrib['value'],
                            level=tree.find('var[@name="level"]').attrib['value'],
                            object_names=tuple(object.attrib['name'] for object in tree.findall('objects/object')))
            results.append(result)
        return results


def zipper(iter):
    for item in iter:
        for subitem in item:
            yield subitem


def process(input_path: Path) -> Iterable[Result]:
    """
    Processes zip files from input_path
    :param input_path: path where zip files are locates
    """
    log.info(f'Processing zip files from {input_path.absolute()}')
    with ProcessPoolExecutor() as pool:
        files = (file for file in input_path.glob('**/*.zip') if file.is_file())
        return zipper(pool.map(process_file, files))

