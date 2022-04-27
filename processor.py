import logging
from concurrent.futures.process import ProcessPoolExecutor
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from typing import Iterator, Any, Optional

from result import Result

log = logging.getLogger(__name__)


def process_archives(input_path: Path, workers: Optional[int] = None) -> Iterator[Result]:
    """
    Processes zip files from input_path
    :param input_path: path where zip files are located
    :param workers: how much workers to use
    :return: iterator with results
    """
    log.info(f'Processing zip files from {input_path.absolute()}')
    with ProcessPoolExecutor(max_workers=workers) as pool:
        files = (file for file in input_path.glob('**/*.zip') if file.is_file())
        yield from _chain(pool.map(process_file, files))


def process_file(path: Path) -> list[Result]:
    """
    Parses each archive
    :return: list with parsing results
    """
    log.info(f'Processing {path}')
    with ZipFile(path) as fp:
        results = []
        for name in fp.namelist():
            tree = etree.fromstring(fp.read(name))
            result = Result(id=tree.find('var[@name="id"]').attrib['value'],
                            level=tree.find('var[@name="level"]').attrib['value'],
                            object_names=tuple(str(object.attrib['name']) for object in tree.findall('objects/object')))
            results.append(result)
        return results


def _chain(iter: Iterator[Any]):
    """
    Helper function for chaining multiple sequences in one sequence
    """
    for item in iter:
        for subitem in item:
            yield subitem
