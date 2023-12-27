from glue_inspector.inspector import GlueInspector

inspector = GlueInspector()
inspector.inspect("dvbt-dataplatformhr-hr-afas-ingress")
inspector.export_sbom("test")
