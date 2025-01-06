# Trivy report

## requirements-glueetl-5.0.txt pip  20 issues


| Package |  Severity | Id | Installed Version  | Fixed Version | Title |
|---------|-----------|----|--------------------|---------------|--------|
| Pygments | MEDIUM | CVE-2022-40896 | 2.7.4 | 2.15.0  | pygments: ReDoS in pygments |
| aiohttp | MEDIUM | CVE-2024-42367 | 3.10.1 | 3.10.2  | aiohttp: python-aiohttp: Compressed files as symlinks are not protected from path traversal |
| aiohttp | MEDIUM | CVE-2024-52304 | 3.10.1 | 3.10.11  | aiohttp: aiohttp vulnerable to request smuggling due to incorrect parsing of chunk extensions |
| cryptography | HIGH | CVE-2023-0286 | 36.0.1 | 39.0.1  | openssl: X.400 address type confusion in X.509 GeneralName |
| cryptography | HIGH | CVE-2023-50782 | 36.0.1 | 42.0.0  | python-cryptography: Bleichenbacher timing oracle attack against RSA decryption - incomplete fix for CVE-2020-25659 |
| cryptography | MEDIUM | CVE-2023-23931 | 36.0.1 | 39.0.1  | python-cryptography: memory corruption via immutable objects |
| cryptography | MEDIUM | CVE-2023-49083 | 36.0.1 | 41.0.6  | python-cryptography: NULL-dereference when loading PKCS7 certificates |
| cryptography | MEDIUM | CVE-2024-0727 | 36.0.1 | 42.0.2  | openssl: denial of service via null dereference |
| cryptography | LOW | GHSA-5cpq-8wj7-hf2v | 36.0.1 | 41.0.0  | Vulnerable OpenSSL included in cryptography wheels |
| cryptography | LOW | GHSA-jm77-qphf-c4w8 | 36.0.1 | 41.0.3  | pyca/cryptography&#39;s wheels include vulnerable OpenSSL |
| cryptography | LOW | GHSA-v8gr-m533-ghj9 | 36.0.1 | 41.0.4  | Vulnerable OpenSSL included in cryptography wheels |
| idna | MEDIUM | CVE-2024-3651 | 2.10 | 3.7  | python-idna: potential DoS via resource consumption via specially crafted inputs to idna.encode() |
| pip | MEDIUM | CVE-2023-5752 | 21.3.1 | 23.3  | pip: Mercurial configuration injectable in repo revision when installing via pip |
| pip | MEDIUM | CVE-2023-5752 | 22.3.1 | 23.3  | pip: Mercurial configuration injectable in repo revision when installing via pip |
| setuptools | HIGH | CVE-2022-40897 | 59.6.0 | 65.5.1  | pypa-setuptools: Regular Expression Denial of Service (ReDoS) in package_index.py |
| setuptools | HIGH | CVE-2024-6345 | 59.6.0 | 70.0.0  | pypa/setuptools: Remote code execution via download functions in the package_index module in pypa/setuptools |
| urllib3 | HIGH | CVE-2021-33503 | 1.25.10 | 1.26.5  | python-urllib3: ReDoS in the parsing of authority part of URL |
| urllib3 | HIGH | CVE-2023-43804 | 1.25.10 | 2.0.6, 1.26.17  | python-urllib3: Cookie request header isn&#39;t stripped during cross-origin redirects |
| urllib3 | MEDIUM | CVE-2023-45803 | 1.25.10 | 2.0.7, 1.26.18  | urllib3: Request body not stripped after redirect from 303 status changes request method to GET |
| urllib3 | MEDIUM | CVE-2024-37891 | 1.25.10 | 1.26.19, 2.2.2  | urllib3: proxy-authorization request header is not stripped during cross-origin redirects |
