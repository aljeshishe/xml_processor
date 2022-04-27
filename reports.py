import csv
import logging
from contextlib import contextmanager
from pathlib import Path

from typing import Iterable, Generator, Optional, ContextManager

from result import Result

log = logging.getLogger(__name__)


def create_reports(results: Iterable[Result], output_path: Path) -> None:
    """
    Creates reports from results
    :param results: results iterator
    :param output_path: path where reports will be placed. Will be created if not exists.
    """
    log.info(f'Creating reports in {output_path.absolute()}')
    output_path.mkdir(parents=True, exist_ok=False)
    with _objects_report_writer(path=output_path) as objects_report:
        with _levels_report_writer(path=output_path) as levels_report:
            for result in results:
                log.info(f'Result {result.level}')
                levels_report.send(result)
                objects_report.send(result)


@contextmanager
def _create_writer(path: Path, field_names) -> csv.DictWriter:
    """
    Helper context manager for creating csv writer
    """
    with path.open('w') as fp:
        writer = csv.DictWriter(f=fp, fieldnames=field_names)
        writer.writeheader()
        yield writer


ResultsReceiver = Generator[None, Optional[Result], None]


def _levels_result_receiver(writer: csv.DictWriter) -> ResultsReceiver:
    """
    Helper coroutine receives Result and writes it to writer
    """
    while True:
        result = yield
        writer.writerow({'id': result.id, 'level': str(result.level)})


def _objects_result_receiver(writer: csv.DictWriter) -> ResultsReceiver:
    """
    Helper coroutine receives Result and writes it to writer
    """
    while True:
        result = yield
        writer.writerows({'id': result.id, 'object_name': name} for name in result.object_names)


@contextmanager
def _levels_report_writer(path: Path):
    """
    Helper context manager for creating level report
    """
    with _create_writer(path=path / 'levels.csv', field_names=['id', 'level']) as writer:
        receiver = _levels_result_receiver(writer)
        receiver.send(None)
        yield receiver


@contextmanager
def _objects_report_writer(path: Path) -> ContextManager[ResultsReceiver]:
    """
    Helper context manager for creating objects report
    """
    with _create_writer(path=path / 'objects.csv', field_names=['id', 'object_name']) as writer:
        receiver = _objects_result_receiver(writer)
        receiver.send(None)
        yield receiver

