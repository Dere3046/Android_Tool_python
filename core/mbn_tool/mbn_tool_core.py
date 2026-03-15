"""MBN tool core implementation."""

from pathlib import Path
from typing import Any, Dict

from common.logging.logger import log_info
from common.parser.mbn.mbn import MBN
from common.parser.parser_image_info_interface import CoreInterface
from common.utils import write_cmdline_file


class MBNToolCore(CoreInterface):
    """MBN tool core class."""

    def __init__(self):
        """Initialize MBN tool core."""
        pass

    def run(self, parsed_args: Dict[str, Any]) -> None:
        """Run MBN tool."""
        subfeature = parsed_args.get('subfeature')

        if subfeature == 'generate':
            with log_info_wrap('generate'):
                self.generate_operation(parsed_args)
        elif subfeature == 'parse':
            with log_info_wrap('parse'):
                self.parse_operation(parsed_args)
        else:
            raise RuntimeError(f"Subfeature '{subfeature}' is unsupported.")

    def generate_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Generate MBN image."""
        mbn_version = parsed_args.get('version', 3)
        data_file = parsed_args.get('data')
        outfile = parsed_args.get('outfile')

        with open(data_file, 'rb') as f:
            code = memoryview(f.read())

        mbn = MBN()
        mbn.create_default(mbn_version, code)

        packed = mbn.pack()

        with open(outfile, 'wb') as f:
            f.write(bytes(packed))

        log_info(f"Generated MBN v{mbn_version} image: {outfile}")

    def parse_operation(self, parsed_args: Dict[str, Any]) -> None:
        """Parse MBN image."""
        infile = parsed_args.get('infile')

        with open(infile, 'rb') as f:
            data = memoryview(f.read())

        mbn = MBN()
        mbn.unpack(data)

        print(mbn)


def log_info_wrap(operation: str):
    """Log info context manager."""
    class LogInfoContext:
        def __enter__(self):
            log_info(f"Starting {operation} operation...")
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is None:
                log_info(f"Completed {operation} operation successfully.")
            else:
                log_warning(f"{operation} operation failed: {exc_val}")
            return False

    return LogInfoContext()
