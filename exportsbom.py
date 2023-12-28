import argparse

from glue_inspector.inspector import GlueInspector


def process_job(jobname, output):
    inspector = GlueInspector()
    if inspector.inspect(jobname):
        inspector.export_sbom(output)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Scan Gluejobs")

    # Add command line arguments
    parser.add_argument("jobname", help="Name of the job to scan")
    parser.add_argument("output", help="Output file")

    # Parse the command line arguments
    args = parser.parse_args()

    # Call the function to process the job
    process_job(args.jobname, args.output)


if __name__ == "__main__":
    main()
