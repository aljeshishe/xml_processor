import tempfile
from pathlib import Path

import mock

from creator import create_archives
from processor import process_archives
from reports import create_reports


@mock.patch('creator._new_id', side_effect=map(str, range(4)))
@mock.patch('creator._new_level', side_effect=map(str, range(4)))
@mock.patch('creator._new_object_name', side_effect=map(str, range(8)))
@mock.patch('creator._objects_count', return_value=2)
def test(_objects_count, _new_object_name, _new_level, _new_id):
    with tempfile.TemporaryDirectory(dir='.') as dir:
        tmp_path = Path(dir)
        create_archives(path=tmp_path, archives_count=2, files_count=2, workers=1)
        results = process_archives(input_path=tmp_path, workers=1)
        create_reports(results=results, output_path=tmp_path)

        actual = (tmp_path / 'levels.csv').read_text()
        expected = (Path(__file__).parent / 'levels.csv').read_text()
        assert actual == expected

        actual = (tmp_path / 'objects.csv').read_text()
        expected = (Path(__file__).parent / 'objects.csv').read_text()
        assert actual == expected
