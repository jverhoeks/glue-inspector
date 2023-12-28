import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import logging


class GlueProvidedPackage:
    url_glueetl = "https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html"
    url_pythonshell = "https://docs.aws.amazon.com/glue/latest/dg/add-job-python.html"

    def __init__(self, cached=True):
        self.packages_list = {}
        self.packages_dict = {}
        self.cached = cached
        self.cache_prefix = "requirements"
        self.glueetl_versions = ["2.0", "3.0", "4.0"]
        self.pythonshell_versions = [
            "3.6",
            "3.9-analytics",
            "3.9",
        ]

    def get(self, type, version):
        print(self.packages_list)
        if f"{type}-{version}" not in self.packages_list == 0:
            if self.cached:
                self.__read(type, version)
            else:
                self.download(type)

        return self.packages_list[f"{type}-{version}"]

    def get_dict(self, type, version):
        print(self.packages_dict)
        if f"{type}-{version}" not in self.packages_dict:
            if self.cached:
                self.__read(type, version)
            else:
                self.download(type)
        return self.packages_dict[f"{type}-{version}"]

    def __convert2dict(self, type, version):
        # convert into dict
        self.packages_dict[f"{type}-{version}"] = {
            p.split("==")[0]: {version: p.split("==")[1]}
            for p in self.packages_list[f"{type}-{version}"]
        }

    def download(self, type):
        """_summary_

        Args:
            type (_type_): _description_
        """
        if type == "pythonshell":
            return self.__download_pythonshell()
        elif type == "glueetl":
            return self.__download_glueetl()
        else:
            logging.error("Invalid Type")
        return False

    def __download_glueetl(self):
        response = requests.get(self.url_glueetl)
        logging.debug(f"Download from {self.url_glueetl}")
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            for version in self.glueetl_versions:
                tabid = "aws-glue-version-" + version
                try:
                    # Find the div with the specified ID
                    target_div = soup.find("dd", {"tab-id": tabid})
                    # Extract packages with '==' from the list items
                    self.packages_list[f"glueetl-{version}"] = [
                        li.get_text()
                        for li in target_div.find_all("li")
                        if "==" in li.get_text()
                    ]

                    self.__convert2dict("glueetl", version)
                    if self.cached:
                        self.__save("glueetl", version)

                except Exception as e:
                    print(e)
                    return False
            return True
        else:
            print("Error Download")
        return False

    def __download_pythonshell(self):
        response = requests.get(self.url_pythonshell)
        logging.debug(f"Download from {self.url_pythonshell}")
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            tabid = "w570aac27c15c15b6"

            try:
                # Find the div with the specified ID
                table_data = []
                target_table = soup.find("table", {"id": tabid})

                for row in target_table.find_all("tr"):
                    # Extract the text from each cell in the row
                    row_data = [
                        cell.get_text(strip=True) for cell in row.find_all(["td"])
                    ]
                    table_data.append(row_data)

                # remove first 2 items
                table_data.pop(0)
                table_data.pop(0)
                print(table_data)

                for index, version in enumerate(self.pythonshell_versions):
                    print(index, version)
                    self.packages_list[f"pythonshell-{version}"] = [
                        f"{t[0]}=={t[index+1]}"
                        for t in table_data
                        if len(t[index + 1]) > 0
                    ]
                    print(f"pythonshell-{version}")
                    print(self.packages_list[f"pythonshell-{version}"])
                    self.__convert2dict("pythonshell", version)
                    if self.cached:
                        self.__save("pythonshell", version)
                return True
            except Exception as e:
                print(e)
                return False

        return False

    def __make_cache_file(self, type, version):
        return f"{self.cache_prefix}-{type}-{version}.txt"

    def __save(self, type, version):
        cache_file = self.__make_cache_file(type, version)
        if len(self.packages_list[f"{type}-{version}"]) > 0:
            # Open the file in write mode
            logging.debug(f"Writing to {cache_file}")
            with open(cache_file, "w") as file:
                file.write("\n".join(self.packages_list[f"{type}-{version}"]))

    def __read(self, type, version):
        cache_file = self.__make_cache_file(type, version)
        print(cache_file)
        try:
            logging.debug(f"Reading from {cache_file}")
            with open(cache_file, "r") as file:
                self.packages_list[f"{type}-{version}"] = file.read().split("\n")
                self.__convert2dict(type, version)
        except Exception as e:
            logging.error(f"Writing to {e}")
            self.download(type)
