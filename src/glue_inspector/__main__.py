#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from glue_inspector.inspector import GlueInspector
from glue_inspector.support import GlueProvidedPackage


def setup_logging(verbose: bool = False) -> None:
    """Configure logging based on verbosity level."""
    level = logging.DEBUG if verbose else logging.INFO
    format = "[%(filename)s:%(lineno)s] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.getLogger("botocore.tokens").setLevel(logging.WARNING)
    logging.basicConfig(level=level, format=format)


def download_config(cache_dir: Optional[Path] = None, force: bool = False) -> bool:
    """
    Download Glue configurations from AWS documentation.

    Args:
        cache_dir: Optional directory to store cached configs
        force: Force download even if cache exists
    """
    try:
        package = GlueProvidedPackage(
            cached=not force, cache_dir=cache_dir if cache_dir else Path.home() / ".glue-inspector"
        )

        # Download both job types
        logging.info("Downloading Glue ETL configurations...")
        if not package.download("glueetl"):
            logging.error("Failed to download Glue ETL configurations")
            return False

        logging.info("Downloading Python Shell configurations...")
        if not package.download("pythonshell"):
            logging.error("Failed to download Python Shell configurations")
            return False

        return True

    except Exception as e:
        logging.error(f"Failed to download configurations: {e}")
        return False


def inspect_job(job_name: str, output_format: str = "sbom", output_file: Optional[Path] = None) -> bool:
    """
    Inspect an AWS Glue job and generate report.

    Args:
        job_name: Name of the Glue job to inspect
        output_format: Format of the output ('sbom' or 'text')
        output_file: Optional file to write output to
    """
    try:
        logging.debug(f"Inspecting Job: {job_name} Output: {output_format}")
        inspector = GlueInspector()

        if not inspector.inspect(job_name):
            logging.error(f"Failed to inspect job: {job_name}")
            return False

        if output_format == "sbom":
            output = inspector.export_sbom(validate=True)
        else:
            output = inspector.export_text()

        if output_file:
            print(f"Writing output to {output_file}")
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(output)
            logging.debug(f"Output written to {output_file}")
        else:
            print(output)

        return True

    except Exception as e:
        print(e)
        logging.error(f"Failed to inspect job: {e}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="AWS Glue Job Inspector - Analyze dependencies and configurations")

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download Glue configurations")
    download_parser.add_argument("--cache-dir", type=Path, help="Directory to store cached configurations")
    download_parser.add_argument("--force", action="store_true", help="Force download even if cache exists")

    # Inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a Glue job")
    inspect_parser.add_argument("job_name", help="Name of the Glue job to inspect")
    inspect_parser.add_argument(
        "--format", choices=["sbom", "text"], default="sbom", help="Output format (default: sbom)"
    )
    inspect_parser.add_argument("--output", type=Path, help="Output file (default: stdout)")

    # Global options
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()
    setup_logging(args.verbose)

    if args.command == "download":
        success = download_config(args.cache_dir, args.force)
    elif args.command == "inspect":
        success = inspect_job(args.job_name, args.format, args.output)
    else:
        parser.print_help()
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
