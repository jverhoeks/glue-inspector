# Trivy report

## requirements-glueetl-2.0.txt pip  30 issues


| Package |  Severity | Id | Installed Version  | Fixed Version | Title |
|---------|-----------|----|--------------------|---------------|--------|
| PyMySQL | CRITICAL | CVE-2024-36039 | 0.9.3 | 1.1.1  | python-pymysql: SQL injection if used with untrusted JSON input |
| PyYAML | CRITICAL | CVE-2020-14343 | 5.3.1 | 5.4  | PyYAML: incomplete fix for CVE-2020-1747 |
| certifi | HIGH | CVE-2023-37920 | 2019.11.28 | 2023.7.22  | python-certifi: Removal of e-Tugra root certificate |
| certifi | MEDIUM | CVE-2022-23491 | 2019.11.28 | 2022.12.07  | python-certifi: untrusted root certificates |
| idna | MEDIUM | CVE-2024-3651 | 2.9 | 3.7  | python-idna: potential DoS via resource consumption via specially crafted inputs to idna.encode() |
| joblib | CRITICAL | CVE-2022-21797 | 0.14.1 | 1.2.0  | The package joblib from 0 and before 1.2.0 are vulnerable to Arbitrary ... |
| mpmath | HIGH | CVE-2021-29063 | 1.1.0 | 1.3.0  | A Regular Expression Denial of Service (ReDOS) vulnerability was disco ... |
| nltk | HIGH | CVE-2021-3828 | 3.5 | 3.6.4  | nltk is vulnerable to Inefficient Regular Expression Complexity |
| nltk | HIGH | CVE-2021-3842 | 3.5 | 3.6.6  | nltk is vulnerable to Inefficient Regular Expression Complexity |
| nltk | HIGH | CVE-2021-43854 | 3.5 | 3.6.6  | NLTK (Natural Language Toolkit) is a suite of open source Python modul ... |
| nltk | HIGH | CVE-2024-39705 | 3.5 | 3.9  | NLTK through 3.8.1 allows remote code execution if untrusted packages  ... |
| numpy | HIGH | CVE-2021-41495 | 1.18.1 | 1.19  | numpy: NULL pointer dereference in numpy.sort in in the PyArray_DescrNew() due to missing return-value validation |
| numpy | MEDIUM | CVE-2021-33430 | 1.18.1 | 1.21  | numpy: buffer overflow in the PyArray_NewFromDescr_int() in ctors.c |
| numpy | MEDIUM | CVE-2021-34141 | 1.18.1 | 1.22  | numpy: incomplete string comparison in the numpy.core component |
| numpy | MEDIUM | CVE-2021-41496 | 1.18.1 | 1.19  | numpy: buffer overflow in the array_from_pyobj() in fortranobject.c |
| pyarrow | CRITICAL | CVE-2023-47248 | 0.16.0 | 14.0.1  | PyArrow: Arbitrary code execution when loading a malicious data file |
| requests | MEDIUM | CVE-2023-32681 | 2.23.0 | 2.31.0  | python-requests: Unintended leak of Proxy-Authorization header |
| requests | MEDIUM | CVE-2024-35195 | 2.23.0 | 2.32.0  | requests: subsequent requests to the same host ignore cert verification |
| scikit-learn | CRITICAL | CVE-2020-13092 | 0.22.1 |   | scikit-learn (aka sklearn) through 0.23.0 can unserialize and execute  ... |
| scikit-learn | MEDIUM | CVE-2024-5206 | 0.22.1 | 1.5.0  | scikit-learn: Possible sensitive data leak |
| setuptools | HIGH | CVE-2022-40897 | 45.2.0 | 65.5.1  | pypa-setuptools: Regular Expression Denial of Service (ReDoS) in package_index.py |
| setuptools | HIGH | CVE-2024-6345 | 45.2.0 | 70.0.0  | pypa/setuptools: Remote code execution via download functions in the package_index module in pypa/setuptools |
| tqdm | LOW | CVE-2024-34062 | 4.64.1 | 4.66.3  | python-tqdm: non-boolean CLI arguments may lead to local code execution |
| urllib3 | HIGH | CVE-2021-33503 | 1.25.8 | 1.26.5  | python-urllib3: ReDoS in the parsing of authority part of URL |
| urllib3 | HIGH | CVE-2023-43804 | 1.25.8 | 2.0.6, 1.26.17  | python-urllib3: Cookie request header isn&#39;t stripped during cross-origin redirects |
| urllib3 | MEDIUM | CVE-2020-26137 | 1.25.8 | 1.25.9  | python-urllib3: CRLF injection via HTTP request method |
| urllib3 | MEDIUM | CVE-2023-45803 | 1.25.8 | 2.0.7, 1.26.18  | urllib3: Request body not stripped after redirect from 303 status changes request method to GET |
| urllib3 | MEDIUM | CVE-2024-37891 | 1.25.8 | 1.26.19, 2.2.2  | urllib3: proxy-authorization request header is not stripped during cross-origin redirects |
| wheel | HIGH | CVE-2022-40898 | 0.35.1 | 0.38.1  | python-wheel: remote attackers can cause denial of service via attacker controlled input to wheel cli |
| zipp | MEDIUM | CVE-2024-5569 | 3.12.0 | 3.19.1  | github.com/jaraco/zipp: Denial of Service (infinite loop) via crafted zip file in jaraco/zipp |
