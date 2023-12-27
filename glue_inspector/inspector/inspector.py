import boto3
import logging
from pprint import pprint


class GlueInspector:
    def __init__(self) -> None:
        """_Initialize"""

    def __get_job(self, job_name):
        glue_client = boto3.client("glue")

        try:
            response = glue_client.get_job(JobName=job_name)
            print(response)

        except Exception as e:
            logging.error(f"Something went wrong querying job: {job_name}")
            return False

        if not "Job" in response:
            logging.error(f"No job information found {job_name}")
            return False

        self.job = response["Job"]
        pprint(self.job)

        # get details
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
            self.modules = self.job["DefaultArguments"][
                "--additional-python-modules"
            ].split(",")
        return True

    def inspect(self, job_name: str):
        """Inspect a glue job

        Args:
            job_name (str): _description_
        """

        if not self.__get_job(job_name):
            print("Error")
            return False

        print("Checking job")

        print(f"{self.glue_type} {self.modules}")

    def export_sbom(self, target):
        """Export the Sbom of the glue job

        Args:
            target (_type_): _description_
        """
