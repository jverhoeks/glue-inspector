import json
import logging
import os
import subprocess
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from markdown_table_generator import Alignment, generate_markdown, table_from_string_list


@dataclass
class VulnerabilityInfo:
    """Data class for storing vulnerability information."""

    vulnerability_id: str
    package_name: str
    installed_version: str
    fixed_version: str
    primary_url: str
    title: str
    severity: str
    published_date: str


class VulnerabilityScanner:
    """Class for scanning and analyzing vulnerabilities in Python packages."""

    VULNERABILITY_KEYS = [
        "VulnerabilityID",
        "PkgName",
        "InstalledVersion",
        "FixedVersion",
        "PrimaryURL",
        "Title",
        "Severity",
        "PublishedDate",
    ]

    def __init__(self, directory: Optional[Path] = None):
        self.directory = directory if directory else Path.home() / ".glue-inspector"
        self.logger = logging.getLogger(__name__)

    def run_trivy_scan(self) -> str:
        """
        Run Trivy scanner and return path to temporary output file.

        Returns:
            str: Path to temporary JSON file containing scan results

        Raises:
            RuntimeError: If Trivy scan fails
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")

        # Sanitize inputs before passing to subprocess
        if not os.path.isdir(self.directory):
            raise ValueError(f"Invalid directory: {self.directory}")

        if not os.path.exists(temp_file.name):
            raise ValueError(f"Invalid temp file path: {temp_file.name}")

        try:
            subprocess.run(
                [
                    "trivy",
                    "fs",
                    self.directory,
                    "--file-patterns",
                    "pip:requirements-.*\\.txt",
                    "--format",
                    "json",
                    "--scanners",
                    "vuln,secret,license",
                    "-d",
                    "--list-all-pkgs",
                    "--output",
                    temp_file.name,
                ],
                check=True,
            )
            return temp_file.name
        except subprocess.CalledProcessError as e:
            temp_file.close()
            os.unlink(temp_file.name)
            raise RuntimeError(f"Trivy scan failed: {e}") from e

    def read_vulnerability_data(self, file_path: str) -> Dict:
        """
        Read and parse vulnerability data from JSON file.

        Args:
            file_path: Path to the JSON file containing vulnerability data

        Returns:
            Dict containing parsed vulnerability data
        """
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            vulns = {}

            for result in data["Results"]:
                if result["Class"] == "lang-pkgs" and result["Type"] == "pip":
                    target = result["Target"]
                    vulns[target] = {}

                    if "Vulnerabilities" in result:
                        vulns[target]["Vulnerabilities"] = [
                            {key: item[key] for key in self.VULNERABILITY_KEYS if key in item}
                            for item in result["Vulnerabilities"]
                        ]

                    if "Packages" in result:
                        vulns[target]["Packages"] = [
                            {key: item[key] for key in ["Name", "Version"] if key in item}
                            for item in result["Packages"]
                        ]

            return vulns

    def merge_package_data(self, vulnerability_data: Dict) -> Dict:
        """
        Merge package data across different requirement files.

        Args:
            vulnerability_data: Raw vulnerability data

        Returns:
            Dict containing merged package data
        """
        merged = {}
        for target, data in vulnerability_data.items():
            if not isinstance(data, dict):
                self.logger.warning(f"Unexpected data format for target {target}")
                continue

            packages = data.get("Packages", [])
            if not isinstance(packages, list):
                self.logger.warning(f"Unexpected packages format for target {target}")
                continue

            for package in packages:
                if not isinstance(package, dict):
                    continue

                name = package.get("Name")
                version = package.get("Version")
                if name:
                    if name not in merged:
                        merged[name] = {}
                    if version:
                        merged[name][target] = version

        return merged

    def merge_vulnerability_data(self, vulnerability_data: Dict) -> Dict:
        """
        Merge vulnerability data for packages.

        Args:
            vulnerability_data: Raw vulnerability data

        Returns:
            Dict containing merged vulnerability information
        """
        merged = defaultdict(lambda: defaultdict(dict))

        for _target, data in vulnerability_data.items():
            if "Vulnerabilities" in data:
                for vuln in data["Vulnerabilities"]:
                    merged[vuln["PkgName"]][vuln["InstalledVersion"]] = vuln

        return merged

    def lookup_vulnerability(self, vulns: Dict, package: str, version: str) -> str:
        """
        Look up vulnerability information for a package version.

        Args:
            vulns: Vulnerability data dictionary
            package: Package name
            version: Package version

        Returns:
            str: Formatted vulnerability information or empty string if none found
        """
        if package in vulns and version in vulns[package] and "VulnerabilityID" in vulns[package][version]:
            vuln = vulns[package][version]
            return f'{vuln["Severity"]} [{vuln["VulnerabilityID"]}]({vuln["PrimaryURL"]})'
        return ""

    def generate_markdown_table(self, package_data: Dict, vulnerability_data: Dict) -> str:
        """
        Generate markdown table from vulnerability data.

        Args:
            package_data: Merged package data
            vulnerability_data: Merged vulnerability data

        Returns:
            str: Generated markdown table
        """
        headers = [
            "Package",
            "2.0",
            "2.0 vuln",
            "3.0",
            "3.0 vuln",
            "4.0",
            "4.0 vuln",
            "5.0",
            "5.0 vuln",
            "shell 3.6",
            "shell 3.6 vuln",
            "shell 3.9",
            "shell 3.9 vuln",
            "shell 3.9 analytics",
            "shell 3.9 analytics vuln",
        ]

        rows = []
        for package, versions in sorted(package_data.items()):
            row = [package]
            for req_file in [
                "requirements-glueetl-2.0.txt",
                "requirements-glueetl-3.0.txt",
                "requirements-glueetl-4.0.txt",
                "requirements-glueetl-5.0.txt",
                "requirements-pythonshell-3.6.txt",
                "requirements-pythonshell-3.9.txt",
                "requirements-pythonshell-3.9-analytics.txt",
            ]:
                version = versions.get(req_file, "")
                row.append(version)
                row.append(self.lookup_vulnerability(vulnerability_data, package, version))
            rows.append(row)

        markdown_data = [headers] + rows
        table = table_from_string_list(markdown_data, Alignment.CENTER)
        return generate_markdown(table)

    def scan_and_report(self) -> str:
        """
        Run complete vulnerability scan and generate report.

        Returns:
            str: Markdown formatted vulnerability report
        """
        try:
            scan_file = self.run_trivy_scan()
            vuln_data = self.read_vulnerability_data(scan_file)
            package_data = self.merge_package_data(vuln_data)
            vulnerability_data = self.merge_vulnerability_data(vuln_data)
            return self.generate_markdown_table(package_data, vulnerability_data)
        finally:
            if "scan_file" in locals():
                os.unlink(scan_file)


def main():
    logging.basicConfig(level=logging.INFO)
    scanner = VulnerabilityScanner()
    print(scanner.scan_and_report())


if __name__ == "__main__":
    main()
