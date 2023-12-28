import json
import logging
from collections import OrderedDict, defaultdict
from pprint import pprint

from markdown_table_generator import (
    Alignment,
    generate_markdown,
    table_from_string_list,
)

# trivy  fs ./ --file-patterns "pip:requirements-.*\.txt" --format json --scanners vuln,config,secret,license -d --output test.json


def read_vuln(file_path):
    # Read JSON from the file into a dictionary
    with open(file_path, "r") as file:
        data = json.load(file)

        keys_to_keep = [
            "VulnerabilityID",
            "PkgName",
            "InstalledVersion",
            "FixedVersion",
            "PrimaryURL",
            "Title",
            "Severity",
            "PublishedDate",
        ]
        vulns = {}
        for v in data["Results"]:
            if v["Class"] == "lang-pkgs" and v["Type"] == "pip":
                vulns[v["Target"]] = {}
                if "Vulnerabilities" in v:
                    vulns[v["Target"]]["Vulnerabilities"] = [
                        {key: item[key] for key in keys_to_keep if key in item}
                        for item in v["Vulnerabilities"]
                    ]
                if "Packages" in v:
                    vulns[v["Target"]]["Packages"] = [
                        {key: item[key] for key in ["Name", "Version"] if key in item}
                        for item in v["Packages"]
                    ]
    return vulns


data = read_vuln("test.json")

merged_dict = {}
for v, d in data.items():
    for p in d["Packages"]:
        if p["Name"] not in merged_dict:
            merged_dict[p["Name"]] = {}
        merged_dict[p["Name"]].update({v: p["Version"]})


merged_vuln = defaultdict(defaultdict)

for ver, d in data.items():
    if "Vulnerabilities" in d:
        for v in d["Vulnerabilities"]:
            merged_vuln[v["PkgName"]][v["InstalledVersion"]] = v


def lookup_vuln(vulns, p, v):
    if p in vulns:
        if v in vulns[p]:
            if "VulnerabilityID" in merged_vuln[p][v]:
                return f'{merged_vuln[p][v]["Severity"]} [{merged_vuln[p][v]["VulnerabilityID"]}]({merged_vuln[p][v]["PrimaryURL"]})'

    return ""


sorted_dict = OrderedDict(sorted(merged_dict.items()))

headers = [
    "Package",
    "2.0",
    "2.0 vuln",
    "3.0",
    "3.0 vuln",
    "4.0",
    "4.0 vuln",
    "shell 3.6",
    "shell 3.6 vuln",
    "shell 3.9",
    "shell 3.9 vuln",
    "shell 3.9 analytics",
    "shell 3.9 analytics vuln",
]

markdown_data = [
    [
        p,
        v.get("requirements-glueetl-2.0.txt", ""),
        lookup_vuln(merged_vuln, p, v.get("requirements-glueetl-2.0.txt", "")),
        v.get("requirements-glueetl-3.0.txt", ""),
        lookup_vuln(merged_vuln, p, v.get("requirements-glueetl-3.0.txt", "")),
        v.get("requirements-glueetl-4.0.txt", ""),
        lookup_vuln(merged_vuln, p, v.get("requirements-glueetl-4.0.txt", "")),
        v.get("requirements-pythonshell-3.6.txt", ""),
        lookup_vuln(merged_vuln, p, v.get("requirements-pythonshell-3.6.txt", "")),
        v.get("requirements-pythonshell-3.9.txt", ""),
        lookup_vuln(merged_vuln, p, v.get("requirements-pythonshell-3.9.txt", "")),
        v.get("requirements-pythonshell-3.9-analytics.txt", ""),
        lookup_vuln(merged_vuln, p, v.get("requirements-pythonshell-3.9-analytics.txt", "")),
    ]
    for p, v in sorted_dict.items()
]

markdown_data.insert(0, headers)
table = table_from_string_list(markdown_data, Alignment.CENTER)
markdown = generate_markdown(table)
print(markdown)
