# Trivy report

## requirements-pythonshell-3.6.txt pip  8 issues


| Package |  Severity | Id | Installed Version  | Fixed Version | Title |
|---------|-----------|----|--------------------|---------------|--------|
| numpy | HIGH | CVE-2021-41495 | 1.16.2 | 1.19  | numpy: NULL pointer dereference in numpy.sort in in the PyArray_DescrNew() due to missing return-value validation |
| numpy | MEDIUM | CVE-2021-33430 | 1.16.2 | 1.21  | numpy: buffer overflow in the PyArray_NewFromDescr_int() in ctors.c |
| numpy | MEDIUM | CVE-2021-34141 | 1.16.2 | 1.22  | numpy: incomplete string comparison in the numpy.core component |
| numpy | MEDIUM | CVE-2021-41496 | 1.16.2 | 1.19  | numpy: buffer overflow in the array_from_pyobj() in fortranobject.c |
| requests | MEDIUM | CVE-2023-32681 | 2.22.0 | 2.31.0  | python-requests: Unintended leak of Proxy-Authorization header |
| requests | MEDIUM | CVE-2024-35195 | 2.22.0 | 2.32.0  | requests: subsequent requests to the same host ignore cert verification |
| scikit-learn | CRITICAL | CVE-2020-13092 | 0.20.3 |   | scikit-learn (aka sklearn) through 0.23.0 can unserialize and execute  ... |
| scikit-learn | MEDIUM | CVE-2024-5206 | 0.20.3 | 1.5.0  | scikit-learn: Possible sensitive data leak |
