import re
import logging


class MergeRequirements:
    def __init__(self):
        """_summary_"""

    def __parse(self, requirements_list):
        """_summary_

        Args:
            requirements_list (List): _description_
        """
        pattern = re.compile(r"^([^\s<>=]+)\s*([<>=]+)\s*([^<>=]+)\s*$")

        requirements = {}

        for line in requirements_list:
            match = pattern.match(line.strip())
            if match:
                package_name, operator, version = match.groups()
                logging.debug(
                    f"Package: {package_name}, Operator: {operator}, Version: {version}"
                )

                requirements[package_name] = {"operator": operator, "version": version}

        return requirements

    def merge(self, first, second, override=True):
        """_summary_

        Args:
            first (_type_): _description_
            second (_type_): _description_
            override (bool, optional): _description_. Defaults to True.
        """

        # convert into dict for comparison
        first_dict = self.__parse(first)
        second_dict = self.__parse(second)

        if override:
            merged = first_dict.copy()
            merged.update(second_dict)
        else:
            # we should match versions here
            merged = first_dict.copy()
            merged.update(second_dict)

        # make it a list again for return
        merged_list = [f"{k}{v['operator']}{v['version']}" for k, v in merged.items()]

        return merged_list
