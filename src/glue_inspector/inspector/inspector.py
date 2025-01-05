import logging

import boto3

from glue_inspector.support import GlueProvidedPackage
from glue_inspector.support.requirements import Requirements
from glue_inspector.support.sbom_generator import SBomGenerator


class GlueInspector:
    def __init__(self) -> None:
        """_Initialize"""

    def __get_job(self, job_name):
        glue_client = boto3.client("glue")
        self.job_name = job_name

        try:
            response = glue_client.get_job(JobName=job_name)

        except Exception as e:
            print(e)
            logging.error(f"Something went wrong querying job: {job_name}")
            return False

        if "Job" not in response:
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

        if "library-set" in self.job["DefaultArguments"]:
            self.library_set = self.job["DefaultArguments"]["library-set"]

        if self.glue_type == "pythonshell":
            if self.library_set:
                self.version = f"{self.python_version}-{self.library_set}"
            else:
                self.version = self.python_version

        elif self.glue_type == "glueetl":
            self.version = self.glue_version
        else:
            self.version = None

        # pythonshell library set

        # extra modules
        if "--additional-python-modules" in self.job["DefaultArguments"]:
            self.modules = self.job["DefaultArguments"]["--additional-python-modules"].split(",")
        else:
            self.modules = None
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
            glue_modules = GlueProvidedPackage().get(self.glue_type, self.version)
            glue_requirements = Requirements(glue_modules)
            # merge them with the provided versions

            self.requirements = Requirements(self.modules)

            self.merged_requirements = glue_requirements.merge(self.requirements)

        elif self.glue_type == "pythonshell":
            glue_modules = GlueProvidedPackage().get(self.glue_type, self.version)
            glue_requirements = Requirements(glue_modules)
            # merge them with the provided versions
            self.requirements = Requirements(self.modules)
            self.merged_requirements = glue_requirements.merge(self.requirements)
        else:
            logging.error("We don't support ray or other types yet")
            return False

        return True

    def export_sbom(self, validate=False):
        """Export the Sbom of the glue job

        Args:
            target (_type_): _description_
        """

        sbom = SBomGenerator(self.job_name, self.merged_requirements)
        sbom.generate()

        return sbom.get_json(validate)

    def export_text(self, target=""):
        """Export the Sbom of the glue job

        Args:
            target (_type_): _description_
        """

        return self.merged_requirements.as_str()
        # join list to make a big string
        # parser = RequirementsParser(self.merged_requirements.as_str())
        # bom = Bom.from_parser(parser=parser)
        # bom.metadata.tools.add(Tool(vendor="CycloneDX", name="test", version="1.0"))

        # output = get_output_instance(
        #     bom=bom,
        #     output_format=OutputFormat.JSON,
        #     schema_version=SchemaVersion["V{}".format(str("1.4").replace(".", "_"))],
        # )

        # pprint(output.output_as_string())
