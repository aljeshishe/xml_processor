from creator import create_archives
from datetime import datetime

from pathlib import Path
from processor import process_archives
import logging
from reports import create_reports


def main():
    logging.basicConfig(level=logging.DEBUG)
    now = datetime.now().strftime('%y%m%d_%H%M%S')

    input_path = Path(f'input_{now}')
    output_path = Path(f'output_{now}')

    create_archives(path=input_path)
    results = process_archives(input_path=input_path)
    create_reports(results=results, output_path=output_path)


if __name__ == '__main__':
    main()
