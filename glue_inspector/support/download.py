import requests
from bs4 import BeautifulSoup
import logging


class GlueProvidedPackage:
    url = "https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html"

    def __init__(self, version, cached=True):
        self.packages_list = []
        self.packages_dict = {}
        self.version = version
        self.cached = cached
        self.cache_file = f"requirements-glue-{version}.txt"

    def get(self):
        if len(self.packages_list) == 0:
            if self.cached:
                self.__read()
            else:
                self.__download()
        return self.packages_list

    def get_dict(self):
        if len(self.packages_dict) == 0:
            if self.cached:
                self.__read()
            else:
                self.__download()
        return self.packages_dict

    def __convert2dict(self):
        # convert into dict
        self.packages_dict = {
            p.split("==")[0]: {self.version: p.split("==")[1]}
            for p in self.packages_list
        }

    def __download(self):
        response = requests.get(self.url)
        logging.debug(f"Download from {self.url}")
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            tabid = "aws-glue-version-" + self.version

            try:
                # Find the div with the specified ID
                target_div = soup.find("dd", {"tab-id": tabid})
                # Extract packages with '==' from the list items
                self.packages_list = [
                    li.get_text()
                    for li in target_div.find_all("li")
                    if "==" in li.get_text()
                ]

                self.__convert2dict()
                if self.cached:
                    self.__save()
                return True
            except Exception as e:
                return False

        return False

    def __save(self):
        if len(self.packages_list) > 0:
            # Open the file in write mode
            logging.debug(f"Writing to {self.cache_file}")
            with open(self.cache_file, "w") as file:
                file.write("\n".join(self.packages_list))

    def __read(self):
        try:
            logging.debug(f"Reading from {self.cache_file}")
            with open(self.cache_file, "r") as file:
                self.packages_list = file.read().split("\n")
                self.__convert2dict()
        except Exception as e:
            logging.error(f"Writing to {e}")
            self.__download()
