from glue_inspector.inspector import GlueInspector

inspector = GlueInspector()
if inspector.inspect("dvbt-dataplatformhr-hr-afas-ingress"):
    inspector.export_sbom("test")
