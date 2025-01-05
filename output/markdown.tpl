# Trivy report 
{{- range . -}}
{{- $failures := len .Vulnerabilities }}


{{- if .Vulnerabilities  }} 

## {{  .Target }} {{ .Type }}  {{ $failures }} issues


| Package |  Severity | Id | Installed Version  | Fixed Version | Title | 
|---------|-----------|----|--------------------|---------------|--------|
{{- range .Vulnerabilities }}
| {{ .PkgName }} | {{ .Vulnerability.Severity }} | {{ .VulnerabilityID }} | {{ .InstalledVersion }} | {{ .FixedVersion }}  | {{ escapeXML .Title }} | 
{{- end }}
{{- else }}
{{- end }}
{{ end }}

