from creator import create
from datetime import datetime

from pathlib import Path
from processor import process
import logging
from reports import create_reports


def main():
    logging.basicConfig(level=logging.DEBUG)
    now = datetime.now().strftime('%y%m%d_%H%M%S')

    src_path = Path(f'input_{now}')
    dst_path = Path(f'output_{now}')

    create(path=src_path)
    results_iter = process(input_path=src_path)
    create_reports(results_iter=results_iter, output_path=dst_path)


if __name__ == '__main__':
    main()
