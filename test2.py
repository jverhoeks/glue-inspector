from pprint import pprint
import json
import logging
from collections import defaultdict
from markdown_table_generator import (
    generate_markdown,
    table_from_string_list,
    Alignment,
)

from glue_inspector.support import GlueProvidedPackage, MergeRequirements

first = ["awswrangler==2.15.1", "xlrd==2.0.1"]
second = ["xlrd>=3.0.1"]


merge = MergeRequirements()
print(merge.merge(first, second))


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

        for v in data["Results"]:
            if v["Target"] == "Python":
                vulns = [
                    {key: item[key] for key in keys_to_keep if key in item}
                    for item in v["Vulnerabilities"]
                ]
    return vulns


versions = ["2.0", "3.0", "4.0"]
pversions = ["3.6", "3.9", "3.9-analytics"]

glue_packages = {}
for v in versions:
    glue_packages[v] = GlueProvidedPackage().get_dict("glueetl", v)


for p in pversions:
    glue_packages[p] = GlueProvidedPackage().get_dict("pythonshell", p)
    print(glue_packages[p])


merged_dict = {}
for v, d in glue_packages.items():
    for key, value in d.items():
        if key not in merged_dict:
            merged_dict[key] = {}
        merged_dict[key].update(value)


glue_vulns = {}
for v in versions:
    glue_vulns[v] = read_vuln("glue" + v + "-vuln.json")

merged_vuln = defaultdict(defaultdict)

for ver, d in glue_vulns.items():
    for v in d:
        merged_vuln[v["PkgName"]][v["InstalledVersion"]] = v


# print table


def lookup_vuln(vulns, p, v):
    if p in vulns:
        if v in vulns[p]:
            if "VulnerabilityID" in merged_vuln[p][v]:
                return f'{merged_vuln[p][v]["Severity"]} [{merged_vuln[p][v]["VulnerabilityID"]}]({merged_vuln[p][v]["PrimaryURL"]})'

    return ""


headers = ["Package", "2.0", "2.0 vuln", "3.0", "3.0 vuln", "4.0", "4.0 vuln"]

markdown_data = [
    [
        p,
        v.get("2.0", ""),
        lookup_vuln(merged_vuln, p, v.get("2.0", "")),
        v.get("3.0", ""),
        lookup_vuln(merged_vuln, p, v.get("3.0", "")),
        v.get("4.0", ""),
        lookup_vuln(merged_vuln, p, v.get("4.0", "")),
    ]
    for p, v in merged_dict.items()
]

markdown_data.insert(0, headers)
table = table_from_string_list(markdown_data, Alignment.CENTER)
markdown = generate_markdown(table)
print(markdown)
