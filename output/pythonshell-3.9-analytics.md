# Trivy report

## requirements-pythonshell-3.9-analytics.txt pip  5 issues


| Package |  Severity | Id | Installed Version  | Fixed Version | Title |
|---------|-----------|----|--------------------|---------------|--------|
| PyMySQL | CRITICAL | CVE-2024-36039 | 1.0.2 | 1.1.1  | python-pymysql: SQL injection if used with untrusted JSON input |
| avro | HIGH | CVE-2023-39410 | 1.11.0 | 1.11.3  | apache-avro: Apache Avro Java SDK: Memory when deserializing untrusted data in Avro Java SDK |
| requests | MEDIUM | CVE-2023-32681 | 2.27.1 | 2.31.0  | python-requests: Unintended leak of Proxy-Authorization header |
| requests | MEDIUM | CVE-2024-35195 | 2.27.1 | 2.32.0  | requests: subsequent requests to the same host ignore cert verification |
| scikit-learn | MEDIUM | CVE-2024-5206 | 1.0.2 | 1.5.0  | scikit-learn: Possible sensitive data leak |
