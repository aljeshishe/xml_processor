import csv
import logging
from pathlib import Path
from result import Result
from typing import Iterable

log = logging.getLogger(__name__)


def report_writer(path: Path, fieldnames):
    with path.open('w') as csvfile:
        writer = csv.DictWriter(f=csvfile, fieldnames=fieldnames)
        writer.writeheader()
        while True:
            rows = yield
            writer.writerows(rows)


def create_reports(results_iter: Iterable[Result], output_path: Path):
    log.info(f'Creating results in {output_path.absolute()}')
    output_path.mkdir(parents=True, exist_ok=False)
    object_names_report = report_writer(path=output_path / 'object_names.csv', fieldnames=['id', 'object_name'])
    object_names_report.send(None)
    levels_report = report_writer(path=output_path / 'levels.csv', fieldnames=['id', 'level'])
    levels_report.send(None)
    for result in results_iter:
        levels_report.send(({'id': result.id, 'level': result.level},))
        object_names_report.send({'id': result.id, 'object_name': name} for name in result.object_names)
