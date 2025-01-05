import logging
import re
from dataclasses import dataclass

from packaging import version


@dataclass
class Requirement:
    """
    Represents a requirement for a package.
    """

    name: str
    version: str
    operator: str

    def __init__(self, line: str):
        """
        Initializes a new instance of the class.

        Args:
            line (str): The input line to be processed.
        """
        self.__parse(line)

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return f"{self.name}{self.operator}{self.version}"

    def __gt__(self, other):
        """
        Returns True if the version of this object is greater than the version of the other object.

        Args:
            other (Requirement): The other object to compare against.

        Returns:
            bool: True if the version of this object is greater than the version of the other
                  object.
        """
        return version.parse(self.version) > version.parse(other.version)

    def __lt__(self, other):
        """
        Returns True if the version of this object is less than the version of the other object.

        Args:
            other (Requirement): The other object to compare against.

        Returns:
            bool: True if the version of this object is less than the version of the other object.
        """
        return version.parse(self.version) < version.parse(other.version)

    def __parse(self, line: str):
        """Parses a line from a requirements file and extracts the package name, operator, and
           version.

        Args:
            line (str): The line from the requirements file to be parsed.

        Returns:
            None
        """
        pattern = re.compile(r"^([^\s<>=]+)\s*([<>=]+)\s*([^<>=]+)\s*$")
        match = pattern.match(line.strip())
        if match:
            package_name, operator, version = match.groups()
            logging.debug(f"Package: {package_name}, Operator: {operator}, Version: {version}")

            self.name = package_name
            self.operator = operator
            self.version = version
        else:
            self.name = None
            self.operator = None
            self.version = None
            logging.error(f"Failed to parse line: {line}")


@dataclass
class Requirements:
    # requirements: list(Requirement)
    data: dict[str, Requirement]

    def __init__(self, data=None):
        self.data = {}

        if isinstance(data, list):
            self.add_lines(data)
        elif isinstance(data, str):
            self.add_line(data)

    def as_str(self):
        """
        Returns a string representation of the data values in the object.

        Returns:
            str: A string representation of the data values.
        """
        return "\n".join([str(r) for r in self.data.values()])

    def as_list(self):
        """
        Returns a list of string representations of the data values.
        """
        return [str(r) for r in self.data.values()]

    def __str__(self):
        """
        Returns a string representation of the object.
        """
        return self.as_str()

    def read(self, file):
        """
        Reads a file containing requirements and populates the data dictionary.

        Args:
            file (str): The path to the file containing requirements.

        Returns:
            None
        """
        with open(file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                req = Requirement(line)
                self.data[req.name] = req

    def write(self, file):
        """
        Write the contents of the object to a file.

        Args:
            file (str): The path of the file to write to.

        Returns:
            None
        """
        with open(file, "w") as f:
            f.write(self.as_str())

    def add(self, req: Requirement):
        """
        Add a requirement to the data dictionary.

        Args:
            req (Requirement): The requirement to be added.

        Returns:
            None
        """
        if isinstance(req, Requirement):
            self.data[req.name] = req
        else:
            raise TypeError

    def add_line(self, line):
        """
        Add a line to the requirements data.

        Args:
            line (str): The line to be added.

        Returns:
            None
        """
        req = Requirement(line)
        self.data[req.name] = req

    def add_lines(self, lines: list[str]):
        """
        Add a line to the requirements data.

        Args:
            lines (List[str]): The lines to be added.

        Returns:
            None
        """
        for line in lines:
            req = Requirement(line)
            self.data[req.name] = req

    def merge(self, reqs):
        """
        Merge two requirements objects.

        Args:
            reqs (Requirements): The requirements object to be merged.

        Returns:
            None

        Raises:
            None
        """
        for req_name, req in reqs.data.items():
            if req_name in self.data.keys():
                # compare versions and keep the highest
                if req > self.data[req_name]:
                    self.data[req_name] = req
            else:
                self.data[req_name] = req
        return self
