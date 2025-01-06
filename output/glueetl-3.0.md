# Trivy report

## requirements-glueetl-3.0.txt pip  42 issues


| Package |  Severity | Id | Installed Version  | Fixed Version | Title |
|---------|-----------|----|--------------------|---------------|--------|
| Pillow | CRITICAL | CVE-2023-50447 | 9.4.0 | 10.2.0  | pillow: Arbitrary Code Execution via the environment parameter |
| Pillow | HIGH | CVE-2023-44271 | 9.4.0 | 10.0.0  | python-pillow: uncontrolled resource consumption when textlength in an ImageDraw instance operates on a long text argument |
| Pillow | HIGH | CVE-2023-4863 | 9.4.0 | 10.0.1  | libwebp: Heap buffer overflow in WebP Codec |
| Pillow | HIGH | CVE-2024-28219 | 9.4.0 | 10.3.0  | python-pillow: buffer overflow in _imagingcms.c |
| Pillow | HIGH | GHSA-56pw-mpj4-fxww | 9.4.0 | 10.0.1  | Bundled libwebp in Pillow vulnerable |
| PyMySQL | CRITICAL | CVE-2024-36039 | 1.0.2 | 1.1.1  | python-pymysql: SQL injection if used with untrusted JSON input |
| aiohttp | HIGH | CVE-2024-23334 | 3.8.3 | 3.9.2  | aiohttp: follow_symlinks directory traversal vulnerability |
| aiohttp | HIGH | CVE-2024-30251 | 3.8.3 | 3.9.4  | aiohttp: DoS when trying to parse malformed POST requests |
| aiohttp | MEDIUM | CVE-2023-37276 | 3.8.3 | 3.8.5  | python-aiohttp: HTTP request smuggling via llhttp HTTP request parser |
| aiohttp | MEDIUM | CVE-2023-47627 | 3.8.3 | 3.8.6  | python-aiohttp: numerous issues in HTTP parser with header parsing |
| aiohttp | MEDIUM | CVE-2023-49081 | 3.8.3 | 3.9.0  | aiohttp: HTTP request modification |
| aiohttp | MEDIUM | CVE-2023-49082 | 3.8.3 | 3.9.0  | aiohttp: CRLF injection if user controls the HTTP method using aiohttp client |
| aiohttp | MEDIUM | CVE-2024-23829 | 3.8.3 | 3.9.2  | python-aiohttp: http request smuggling |
| aiohttp | MEDIUM | CVE-2024-27306 | 3.8.3 | 3.9.4  | aiohttp: XSS on index pages for static file handling |
| aiohttp | MEDIUM | CVE-2024-42367 | 3.8.3 | 3.10.2  | aiohttp: python-aiohttp: Compressed files as symlinks are not protected from path traversal |
| aiohttp | MEDIUM | CVE-2024-52304 | 3.8.3 | 3.10.11  | aiohttp: aiohttp vulnerable to request smuggling due to incorrect parsing of chunk extensions |
| aiohttp | MEDIUM | GHSA-pjjw-qhg8-p2p9 | 3.8.3 | 3.8.6  | aiohttp has vulnerable dependency that is vulnerable to request smuggling |
| certifi | HIGH | CVE-2023-37920 | 2021.5.30 | 2023.7.22  | python-certifi: Removal of e-Tugra root certificate |
| certifi | MEDIUM | CVE-2022-23491 | 2021.5.30 | 2022.12.07  | python-certifi: untrusted root certificates |
| certifi | LOW | CVE-2024-39689 | 2021.5.30 | 2024.07.04  | python-certifi: Remove root certificates from `GLOBALTRUST` from the root store |
| idna | MEDIUM | CVE-2024-3651 | 2.10 | 3.7  | python-idna: potential DoS via resource consumption via specially crafted inputs to idna.encode() |
| joblib | CRITICAL | CVE-2022-21797 | 1.0.1 | 1.2.0  | The package joblib from 0 and before 1.2.0 are vulnerable to Arbitrary ... |
| mpmath | HIGH | CVE-2021-29063 | 1.2.1 | 1.3.0  | A Regular Expression Denial of Service (ReDOS) vulnerability was disco ... |
| nltk | HIGH | CVE-2021-3828 | 3.6.3 | 3.6.4  | nltk is vulnerable to Inefficient Regular Expression Complexity |
| nltk | HIGH | CVE-2021-3842 | 3.6.3 | 3.6.6  | nltk is vulnerable to Inefficient Regular Expression Complexity |
| nltk | HIGH | CVE-2021-43854 | 3.6.3 | 3.6.6  | NLTK (Natural Language Toolkit) is a suite of open source Python modul ... |
| nltk | HIGH | CVE-2024-39705 | 3.6.3 | 3.9  | NLTK through 3.8.1 allows remote code execution if untrusted packages  ... |
| numpy | MEDIUM | CVE-2021-33430 | 1.19.5 | 1.21  | numpy: buffer overflow in the PyArray_NewFromDescr_int() in ctors.c |
| numpy | MEDIUM | CVE-2021-34141 | 1.19.5 | 1.22  | numpy: incomplete string comparison in the numpy.core component |
| pip | MEDIUM | CVE-2023-5752 | 23.0 | 23.3  | pip: Mercurial configuration injectable in repo revision when installing via pip |
| pyarrow | CRITICAL | CVE-2023-47248 | 5.0.0 | 14.0.1  | PyArrow: Arbitrary code execution when loading a malicious data file |
| requests | MEDIUM | CVE-2023-32681 | 2.23.0 | 2.31.0  | python-requests: Unintended leak of Proxy-Authorization header |
| requests | MEDIUM | CVE-2024-35195 | 2.23.0 | 2.32.0  | requests: subsequent requests to the same host ignore cert verification |
| scikit-learn | HIGH | CVE-2020-28975 | 0.24.2 | 1.0.1  | scikit-learn Denial of Service |
| scikit-learn | MEDIUM | CVE-2024-5206 | 0.24.2 | 1.5.0  | scikit-learn: Possible sensitive data leak |
| tqdm | LOW | CVE-2024-34062 | 4.64.1 | 4.66.3  | python-tqdm: non-boolean CLI arguments may lead to local code execution |
| urllib3 | HIGH | CVE-2021-33503 | 1.25.11 | 1.26.5  | python-urllib3: ReDoS in the parsing of authority part of URL |
| urllib3 | HIGH | CVE-2023-43804 | 1.25.11 | 2.0.6, 1.26.17  | python-urllib3: Cookie request header isn&#39;t stripped during cross-origin redirects |
| urllib3 | MEDIUM | CVE-2023-45803 | 1.25.11 | 2.0.7, 1.26.18  | urllib3: Request body not stripped after redirect from 303 status changes request method to GET |
| urllib3 | MEDIUM | CVE-2024-37891 | 1.25.11 | 1.26.19, 2.2.2  | urllib3: proxy-authorization request header is not stripped during cross-origin redirects |
| wheel | HIGH | CVE-2022-40898 | 0.37.0 | 0.38.1  | python-wheel: remote attackers can cause denial of service via attacker controlled input to wheel cli |
| zipp | MEDIUM | CVE-2024-5569 | 3.12.0 | 3.19.1  | github.com/jaraco/zipp: Denial of Service (infinite loop) via crafted zip file in jaraco/zipp |
