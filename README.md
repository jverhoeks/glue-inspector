# Glue inspector

Inspects Glue Jobs packages and generates an SBOM

## Steps

1. Download the list of provides packages from the AWS documentation and convert into a requirements.txt
2. Inspects the parameters from the Glue Job to get the job type: (pythonshell/glueetl), glue version , python version.
3. Inspects the jobs of pythonshell libraries are userd
4. Inspect the extra packages configured
5. Merged all the requirements into a single file
6. Exports this as an Sbom


## Howto Run

First install UV by following the instructions here: <https://docs.astral.sh/uv/getting-started/installation/>.
Uv is the new fast python package and project manager. It runs automatic in a virtualenv.


### Download

Test if you can download the configuration from aws

* Glue Etl <https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html>
* Python Shell  <https://docs.aws.amazon.com/glue/latest/dg/add-job-python.html>

```sh
uv run glue-inspector download
```

This will convert the website info into requirements.txt files and store them into ~/.glue_inspector


### Inspect

Set your AWS Credentials in the enviroment: (AWS_PROFILE or AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY) and the correct region.

Run this tool:

```sh
uv run glue-inspector inspect mygluejob --output mygluejob-sbom.json
```

Now you have an sbom in CycloneDX format, with packages from your glue job.  This doesn't contain yet vulnerabilities, you can use trivy or any other tool to scan this file



## Trivy

Check the output file with trivy.  Trivy is an opensource tools from Aqua and can be found here: <https://trivy.dev/latest/getting-started/>

```sh
trivy sbom  mygluejob-sbom.json --scanners vuln,license --list-all-pkgs -d --format table
```

Or create a new sbom with vulnerabilities included:

```sh
trivy sbom  mygluejob-sbom.json --scanners vuln,license --list-all-pkgs -d --format cyclonedx --output  mygluejob-sbom-trivy.json
```



## Website reporting

I like to write blogpoosts about this. I have included a tool that combine the vulnerabilties into a markdown table:


```sh
uv run src/glue_inspector/report/generate-table.py > output.md
```

The output are also included in the [output directory](output/)


filename | critical | high | medium | low | information
-------- | -------- | ---- | ------ | --- | ----------
[glueetl-2.0](output/glueetl-2.0.md) | 5 | 12 | 12 | 1 | 0
[glueetl-3.0](output/glueetl-3.0.md) | 4 | 16 | 20 | 2 | 0
[glueetl-4.0](output/glueetl-4.0.md) | 4 | 14 | 18 | 2 | 0
[glueetl-5.0](output/glueetl-5.0.md) | 0 | 6 | 11 | 3 | 0
[pythonshell-3.6](output/pythonshell-3.6.md) | 1 | 1 | 6 | 0 | 0
[pythonshell-3.9](output/pythonshell-3.9.md) | 0 | 0 | 0 | 0 | 0
[pythonshell-3.9-analytics](output/pythonshell-3.9-analytics.md) | 1 | 1 | 3 | 0 | 0


## Status

### Done

* moved from poetry to uv
* fixed pythonshell support
* added glueetl 5
* converted the table generator into a better program

### Todo


* lookup licences from the packages in pypi
* upload as pypi packages
* support packages from internal repos
* support manual packages from s3
* ???
