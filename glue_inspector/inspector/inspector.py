import logging
from pprint import pprint

import boto3
from cyclonedx.model import Tool
from cyclonedx.model.bom import Bom
from cyclonedx.output import BaseOutput, OutputFormat, SchemaVersion
from cyclonedx.output import get_instance as get_output_instance
from cyclonedx_py.parser.requirements import RequirementsParser

from glue_inspector.support import GlueProvidedPackage, MergeRequirements


class GlueInspector:
    def __init__(self) -> None:
        """_Initialize"""

    def __get_job(self, job_name):
        glue_client = boto3.client("glue")

        try:
            response = glue_client.get_job(JobName=job_name)

        except Exception as e:
            print(e)
            logging.error(f"Something went wrong querying job: {job_name}")
            return False

        if not "Job" in response:
            logging.error(f"No job information found {job_name}")
            return False

        # save the job info
        self.job = response["Job"]

        # split out the  details
        self.python_version = self.job["Command"]["PythonVersion"]
        self.glue_type = self.job["Command"]["Name"]

        if "GlueVersion" in self.job:
            self.glue_version = self.job["GlueVersion"]
        else:
            self.glue_version = None

        # pythonshell library set
        if "library-set" in self.job["DefaultArguments"]:
            self.library_set = job["DefaultArguments"]["library-set"]

        # extra modules
        if "--additional-python-modules" in self.job["DefaultArguments"]:
            self.modules = self.job["DefaultArguments"]["--additional-python-modules"].split(",")
        return True

    def inspect(self, job_name: str):
        """Inspect a glue job

        Args:
            job_name (str): _description_
        """

        if not self.__get_job(job_name):
            print("Error")
            return False

        if self.glue_type == "glueetl":
            # get the default packages from website or cache
            glue_modules = GlueProvidedPackage().get(self.glue_type, self.glue_version)
            # merge them with the provided versions
            self.merged_modules = MergeRequirements().merge(glue_modules, self.modules)

        elif self.glue_type == "pythonshell":
            print("Checking with library")
        else:
            logging.error("We don't support ray or other types yet")
            return False

    def export_sbom(self, target):
        """Export the Sbom of the glue job

        Args:
            target (_type_): _description_
        """

        # join list to make a big string
        parser = RequirementsParser("\n".join(self.merged_modules))
        bom = Bom.from_parser(parser=parser)
        bom.metadata.tools.add(Tool(vendor="CycloneDX", name="test", version="1.0"))

        output = get_output_instance(
            bom=bom,
            output_format=OutputFormat.JSON,
            schema_version=SchemaVersion["V{}".format(str("1.4").replace(".", "_"))],
        )

        pprint(output.output_as_string())
